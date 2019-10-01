# Author: Aidan Kierans

import pandas as pd
from math import sqrt
from multiprocessing import Pool

# Make the data sets into DataFrames
df05 = pd.read_csv('dataset_missing05.csv')
df20 = pd.read_csv('dataset_missing20.csv')
df_complete = pd.read_csv('dataset_complete(1).csv')

# Convert the first eight columns to float64s, and the ?s into NaNs for pandas
df05['F1'] = pd.to_numeric(df05['F1'], errors='coerce')
df05['F2'] = pd.to_numeric(df05['F2'], errors='coerce')
df05['F3'] = pd.to_numeric(df05['F3'], errors='coerce')
df05['F4'] = pd.to_numeric(df05['F4'], errors='coerce')
df05['F5'] = pd.to_numeric(df05['F5'], errors='coerce')
df05['F6'] = pd.to_numeric(df05['F6'], errors='coerce')
df05['F7'] = pd.to_numeric(df05['F7'], errors='coerce')
df05['F8'] = pd.to_numeric(df05['F8'], errors='coerce')

df20['F1'] = pd.to_numeric(df20['F1'], errors='coerce')
df20['F2'] = pd.to_numeric(df20['F2'], errors='coerce')
df20['F3'] = pd.to_numeric(df20['F3'], errors='coerce')
df20['F4'] = pd.to_numeric(df20['F4'], errors='coerce')
df20['F5'] = pd.to_numeric(df20['F5'], errors='coerce')
df20['F6'] = pd.to_numeric(df20['F6'], errors='coerce')
df20['F7'] = pd.to_numeric(df20['F7'], errors='coerce')
df20['F8'] = pd.to_numeric(df20['F8'], errors='coerce')

# set precision to five digits after the decimal point
df05 = df05.round(decimals=5)
df20 = df20.round(decimals=5)
df_complete = df_complete.round(decimals=5)

# mean imputation
df05_mean = df05.fillna(df05.mean())
df20_mean = df20.fillna(df20.mean())


# conditional mean imputation
# add the original index of each row to the df so that they can be put back in this order later
df05.reset_index(inplace=True)
df20.reset_index(inplace=True)


# sort the rows of a df back into the original order, then drop the 'index' column
def reset_order(df):
    return df.sort_values('index').filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])


# split each df into a separate df for each condition - this could probably be optimized
df05_yes = df05.groupby('Class').get_group('Yes')
df05_no = df05.groupby('Class').get_group('No')
df20_yes = df20.groupby('Class').get_group('Yes')
df20_no = df20.groupby('Class').get_group('No')

df05_c_mean = df05_yes.fillna(df05_yes.mean()).append(df05_no.fillna(df05_no.mean()))
df20_c_mean = df20_yes.fillna(df20_yes.mean()).append(df20_no.fillna(df20_no.mean()))

df05_c_mean = reset_order(df05_c_mean)
df20_c_mean = reset_order(df20_c_mean)


# hot deck imputation
# calculate the euclidean distances between two rows
def distance(row1, row2, mask):
    # remove columns with missing values, convert rows from series to lists here if I need to.
    r1 = row1.loc[mask]  # .to_list()
    r2 = row2.loc[mask]  # .to_list()
    # compute and return the euclidean distance between the rows
    if r1.size > 0:
        return sqrt(sum([(x - y) ** 2 for x, y in zip(r1, r2)])) / r1.size
    else:
        return 1


def hot_deck(df):
    df_hd = df.copy()
    df = df.filter(like='F', axis=1)
    df_temp = df.assign(Distance=1.0)
    for i in df.iterrows():
        # make sure this row has missing values in the first place before trying to impute them
        if i[1].hasnans:
            # find the distance between i and each other row
            for j in df.iterrows():
                # skip this iteration if i and j are the same row; i is as far as possible from itself by default
                if i[0] == j[0]:
                    continue
                # form a boolean mask that's true for each column that i and j both have a value in
                match = i[1].notna() & j[1].notna()
                # pass i, j, and the mask to distance() and add the result to the Distance column of df_temp
                df_temp.at[j[0], 'Distance'] = distance(i[1], j[1], match)
            # sort the resulting data so that the shortest distance is moved to the top and i is at the bottom
            df_temp = df_temp.sort_values('Distance')
            # pick the available values from the closest row until i is filled
            for k in df_temp.iterrows():
                # if the ith row of the df still has missing values...
                if df_hd.loc[i[0]].hasnans:
                    # ...keep trying to impute them
                    temp = df_hd.loc[i[0]].combine_first(k[1])
                    df_hd.loc[i[0]] = temp
                else:
                    break
        # if i[0] % 500 == 0:
            # print("i[0]: " + str(i[0]))
    return df_hd


def set_df05_hd():
    # print("Finding df05_hd")
    df = hot_deck(df05)
    df.round(decimals=5).to_csv('V00819990_missing05_imputed_hd.csv', index=False)


def set_df20_hd():
    # print("Finding df20_hd")
    df = hot_deck(df20)
    df.round(decimals=5).to_csv('V00819990_missing20_imputed_hd.csv', index=False)


# conditional hot deck imputation
def set_df05_chd():
    print("Finding df05_chd")
    df = reset_order(hot_deck(df05_yes).append(hot_deck(df05_no)))
    df.round(decimals=5).to_csv('V00819990_missing05_imputed_hd_conditional.csv', index=False)


def set_df20_chd():
    print("Finding df20_chd")
    df = reset_order(hot_deck(df20_yes).append(hot_deck(df20_no)))
    df.round(decimals=5).to_csv('V00819990_missing20_imputed_hd_conditional.csv', index=False)


# impute asynchronously
if __name__ == '__main__':
    pool = Pool(processes=2)

    # Start each process
    pr05hd = pool.apply_async(set_df05_hd)
    pr20hd = pool.apply_async(set_df20_hd)
    pr05chd = pool.apply_async(set_df05_chd)
    pr20chd = pool.apply_async(set_df20_chd)

    pool.close()
    pool.join()

    # calculation of mean absolute error
    # if not for this assignment's constraint that the code must be in a .py file, mean_ae would be Cython
    def mean_ae(df_missing, df_imputed, df_correct):
        ae = 0
        count = 0
        df_missing = df_missing.filter(like='F', axis=1)
        df_imputed = df_imputed.filter(like='F', axis=1)
        df_correct = df_correct.filter(like='F', axis=1)
        for r in df_missing.iterrows():
            for item in r[1].iteritems():
                ae += abs(df_imputed.at[r[0], item[0]] - df_correct.at[r[0], item[0]])
                count += 1
                # Divide the sum of errors by the number of errors, and round to the nearest ten-thousandth
        return round(ae/count, 4)

    # Load the hot-deck-imputed data back into Dataframes
    df05_hd = pd.read_csv('V00819990_missing05_imputed_hd.csv')
    df20_hd = pd.read_csv('V00819990_missing20_imputed_hd.csv')
    df05_chd = pd.read_csv('V00819990_missing05_imputed_hd_conditional.csv')
    df20_chd = pd.read_csv('V00819990_missing20_imputed_hd_conditional.csv')

    # make sure the dfs only include the columns they started with
    df05_mean = df05_mean.filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])
    df05_c_mean = df05_c_mean.filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])
    df05_hd = df05_hd.filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])
    df05_chd = df05_chd.filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])
    df20_mean = df20_mean.filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])
    df20_c_mean = df20_c_mean.filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])
    df20_hd = df20_hd.filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])
    df20_chd = df20_chd.filter(items=['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'Class'])

    # output each imputed df to csv (but first print mea and make sure that they have the right number of digits)
    print(f"MAE_05_mean = " + str(mean_ae(df05, df05_mean, df_complete)))
    df05_mean.round(decimals=5).to_csv('V00819990_missing05_imputed_mean.csv', index=False)

    print("MAE_05_mean_conditional = " + str(mean_ae(df05, df05_c_mean, df_complete)))
    df05_c_mean.round(decimals=5).to_csv('V00819990_missing05_imputed_mean_conditional.csv', index=False)

    print("MAE_05_hd = " + str(mean_ae(df05, df05_hd, df_complete)))

    print("MAE_05_hd_conditional = " + str(mean_ae(df05, df05_chd, df_complete)))

    print("MAE_20_mean = " + str(mean_ae(df20, df20_mean, df_complete)))
    df20_mean.round(decimals=5).to_csv('V00819990_missing20_imputed_mean.csv', index=False)

    print("MAE_20_mean_conditional = " + str(mean_ae(df20, df20_c_mean, df_complete)))
    df20_c_mean.round(decimals=5).to_csv('V00819990_missing20_imputed_mean_conditional.csv', index=False)

    print("MAE_20_hd = " + str(mean_ae(df20, df20_hd, df_complete)))

    print("MAE_20_hd_conditional = " + str(mean_ae(df20, df20_chd, df_complete)))
