import os
from itertools import cycle

from pandas import DataFrame
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib as mpl

def get_relevance_judgements():
    '''
    Retrieves a query number, relevant documents dictionary
    '''
    f = open('cacm.rel.txt','r')
    rl = f.read().splitlines()
    output = {}
    for line in rl:
        split = line.split()
        if output.get(split[0]):
            output[split[0]].add(split[2])
        else:
            output[split[0]] = set()
            output[split[0]].add(split[2])
    return output

def calculate_mrr_and_map(rr_index, p_index):
    '''
    Calculates the Mean Reciprocal ranks and Mean Average Precisions for all runs
    :param rr_index: index of run, reciprocal ranks per query
    :param p_index: index of run to precision dictionaries per query
    '''
    mrrs = {}
    maps = {}
    for run_name in rr_index:
        mrrs[run_name] = 0
        maps[run_name] = 0

        for query in rr_index[run_name]:
            mrrs[run_name] += rr_index[run_name][query]

            ap = 0
            last_p_value = 0
            total_precision_changes = 0
            for p in p_index[run_name][query]:
                if p_index[run_name][query][p] != last_p_value:
                    last_p_value = p_index[run_name][query][p]
                    ap += p_index[run_name][query][p]
                    total_precision_changes += 1

            ap = ap / total_precision_changes

            maps[run_name] += ap


        mrrs[run_name] = mrrs[run_name]/len(rr_index[run_name])
        maps[run_name] = maps[run_name]/len(p_index[run_name])
    return mrrs, maps


def calculate_mean(dict_precisions):
    '''
    calculate mean from values for a series(dictionary) in a dictionary
    :param dict_precisions: input dictionary containing dictionaries as values to calculate means for
    :return: the mean
    '''
    aggregate = Counter()
    total = len(dict_precisions)
    for k in dict_precisions.keys():
        aggregate += Counter(dict_precisions[k])
    mean_dict = dict((k, v/total) for k, v in aggregate.items())
    return mean_dict


def add_to_scatter(retrieval_type, precision_index, recall_index, ax1, line):
    '''
    Given a precision and recall index, add the values to a given axis with specified line type.
    '''
    data = precision_index[retrieval_type]
    data2 = recall_index[retrieval_type]

    mean_precision = calculate_mean(data)
    mean_recall = calculate_mean(data2)

    pvr = {retrieval_type: mean_precision, "recall": mean_recall}
    df = DataFrame(pvr)

    ax1.scatter(df["recall"],df[retrieval_type], s=6,label='_nolegend_')
    ax1.plot(df["recall"], df[retrieval_type],line)


def plot_precision_vs_recall(precision_index, recall_index, file_name):
    '''
    Plotting the precision vs recall for given index and saves the plot to the specified filename.
    '''
    retreival_types = precision_index.keys()
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(111)
    lines = ["-","--",":","-."]
    linecycler = cycle(lines)
    for type in retreival_types:
        add_to_scatter(type, precision_index, recall_index, ax1, next(linecycler))
    plt.legend(loc="upper right", title="Retrieval Method", fontsize="small")
    plt.suptitle("Precision vs Recall")
    plt.xlabel("Mean AVG Recall")
    plt.ylabel("Mean AVG Precision")
    #plt.show()
    fig.savefig(file_name)


def plot_mrrs_maps(mrrs, maps):
    '''
    Generate a bar plot for given MRRS and MAPS with table and save it to a file.
    '''
    df = DataFrame.from_dict(mrrs, orient='index', columns=['MRRS'])
    df2 = DataFrame.from_dict(maps, orient='index', columns=['MAPS'])
    fig, axs = plt.subplots(2,1, figsize=(12,8),  gridspec_kw = {'height_ratios':[3, 1]})
    mpl.style.use('fivethirtyeight')
    df3 = df.join(df2, sort=False, how='outer')
    df4 = df3.transpose()
    df3[["MAPS", "MRRS"]].plot.bar(rot='45', fontsize=12, subplots=False, ax=axs[0])
    #ax1.legend(loc=2)
    plt.suptitle("MAPS and MRR")
    plt.subplots_adjust(left=0.1)
    df4 = df4.round(3)
    axs[0].xaxis.set_visible(False)
    table = axs[1].table(cellText=df4.values, rowLabels=df4.index, colLabels=df4.columns, loc="top")
    axs[1].axis('off')
    table.auto_set_font_size(False)
    table.set_fontsize(7)
    plt.autoscale()
    fig.savefig("figures/MAPS_MRR")


def calculate_p_per_query(precision_index):
    '''
    Calculates precision for each query per model given a precision-index.
    '''
    type_means = DataFrame()
    retreival_types = precision_index.keys()
    for type in retreival_types:
        precisions = precision_index[type]
        precisions = DataFrame.from_dict(precisions)
        means = precisions.mean()
        means.index = means.index.astype(int)
        type_means[type] = means.sort_index()
    return type_means

def calculate_p_at_k(precision_index):
    '''
    Calculates precision at a model level (average for all queries) given a precision-index.
    '''
    type_means = DataFrame()
    retreival_types = precision_index.keys()
    for type in retreival_types:
        precisions = precision_index[type]
        precisions = DataFrame.from_dict(precisions)
        means = precisions.mean(axis=1)
        means.index = means.index.astype(int)
        type_means[type] = means.sort_index()
    return type_means


def plot_p_per_query(p_per_query, name):
    '''
    Plots precision per query and writes to given name.
    '''
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(111)
    p_per_query.plot.bar(rot=0,subplots=False,fontsize=6, ax=ax1)
    plt.suptitle("Relevance for Different Queries")
    plt.xlabel("Query#")
    plt.ylabel("Mean Average Precision")
    plt.legend(loc="upper left", title="Retrieval Method", fontsize="x-small")
    plt.savefig(name)


def generate_tables(precision_index, recall_index):
    '''
    Generate tables for precision and recall at a query level for given precision and recall indicies.
    :return:
    '''
    retreival_types = precision_index.keys()
    for type in retreival_types:
        precisions = DataFrame.from_dict(precision_index[type])
        precisions.columns = precisions.columns.astype(int)
        recalls = DataFrame.from_dict(recall_index[type])
        recalls.columns = recalls.columns.astype(int)
        recalls = recalls.sort_index(axis=1)
        precisions = precisions.sort_index(axis=1)
        precisions.to_csv('figures/precision_recall/' + type + '_precisions.csv')
        recalls.to_csv('figures/precision_recall/' + type + '_recalls.csv')


def plot_r_per_query(r_per_query, name):
    '''
    Plot recall per query and write to file.
    '''
    fig = plt.figure(figsize=(8,8))
    ax1 = fig.add_subplot(111)
    r_per_query.plot.bar(rot=0,subplots=False,fontsize=6, ax=ax1)
    plt.suptitle("Relevance for Different Queries")
    plt.xlabel("Query#")
    plt.ylabel("Recall")
    plt.legend(loc="upper left", title="Retrieval Method", fontsize="x-small")
    plt.savefig(name)


def main():
    '''

    :return:
    '''
    precision_delta_index = {}
    precision_index = {}
    recall_index = {}
    reciprocal_ranks = {}
    rel_judgments = get_relevance_judgements()
    for filename in os.listdir('Outputs'):
        if 'stemmed' in filename:
            continue
        else:
            base_filename = filename[:len(filename) - 4]
            split_filename = base_filename.split('_')
            query_no = split_filename[1]
            if query_no not in rel_judgments:
                continue
            else:
                if len(split_filename) > 2:
                    reference_name = '_'.join([split_filename[0]] + split_filename[2:])
                else:
                    reference_name = split_filename[0]


                if not precision_index.get(reference_name):
                    precision_index[reference_name] = {}

                if not precision_delta_index.get(reference_name):
                    precision_delta_index[reference_name] = {}

                if not recall_index.get(reference_name):
                    recall_index[reference_name] = {}

                f = open('./Outputs/'+filename, 'r')
                rl = f.read().splitlines()
                precision_delta = {}
                precision= {}
                recall = {}
                query_rel_judgements = rel_judgments[query_no]
                relevant_docs_so_far = 0
                i = 1
                for line in rl:
                    split = line.split()
                    if split[2] in query_rel_judgements:
                        relevant_docs_so_far += 1
                        if relevant_docs_so_far == 1:
                            try:
                                reciprocal_ranks[reference_name][query_no] = 1/i
                            except:
                                reciprocal_ranks[reference_name] = {}
                                reciprocal_ranks[reference_name][query_no] = 1/i
                        precision_delta[i] = relevant_docs_so_far / i
                    precision[i] = relevant_docs_so_far / i
                    recall[i] = relevant_docs_so_far / len(query_rel_judgements)
                    i += 1
                precision_index[reference_name][query_no] = precision
                precision_delta_index[reference_name][query_no] = precision_delta
                recall_index[reference_name][query_no] = recall

    mrrs, maps = calculate_mrr_and_map(reciprocal_ranks, precision_delta_index)

    plot_mrrs_maps(mrrs, maps)
    plot_precision_vs_recall(precision_delta_index, recall_index,"figures/mean_avgPrecision@Delta_vs_Recall")
    plot_precision_vs_recall(precision_index, recall_index,"figures/mean_avgPrecision_vs_Recall")
    p_per_query = calculate_p_per_query(precision_index)
    r_per_query = calculate_p_per_query(recall_index)
    p_per_query.to_csv('figures/p_per_query.csv')
    r_per_query.to_csv('figures/r_per_query.csv')
    p_at_k = calculate_p_at_k(precision_index)
    p_at_k.to_csv('figures/p_at_k.csv')
    p_at_k.loc[[5,20]].to_csv('figures/p_at_k5_k20.csv')
    plot_p_per_query(p_per_query, 'figures/p_per_query')
    plot_r_per_query(r_per_query, 'figures/r_per_query')

    generate_tables(precision_index, recall_index)




    plt.show()

if __name__ == '__main__':
    main()
