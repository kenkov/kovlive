#include <iostream>
#include <cstdio>
#include <string>
#include <fstream>
#include <string>
#include <stack>
#include <vector>
#include <utility> // pair
#include <map>
#include <boost/algorithm/string.hpp>

using namespace std;


void train(
        const char* filename,
        const string start_symbol = "<s>",
        const string end_symbol = "</s>"
) {
    ifstream datafs(filename);
    string line;
    map< pair<string, string>, long> bigram;
    map<string, long> unigram;

    long total = 0;

    while (getline(datafs, line)) {
        vector<string> words_without_symbol, words;
        boost::algorithm::split(words_without_symbol, line, boost::is_space());

        // create words vector
        words.push_back(start_symbol);
        for (auto word : words_without_symbol) {
            words.push_back(word);
        }
        words.push_back(end_symbol);

        for (unsigned long i = 0; i < words.size() - 1; i++) {
            bigram[make_pair(words[i], words[i+1])] += 1;
            unigram[words[i]] += 1;
            if (i != 0) {
                // start symbol は unigram モデルには含めない
                total += 1;
            }
        }
        unigram[end_symbol] += 1;
        total += 1;
    }

    for (auto item : bigram) {
        printf("%s %s\t%f\n",
               item.first.first.c_str(),
               item.first.second.c_str(),
               (double) item.second / unigram[item.first.first]
        );
    }

    for (auto item : unigram) {
        string word = item.first;
        if (word != start_symbol) {
            printf("%s\t%f\n",
                    word.c_str(),
                   (double) item.second / total
            );
        }
    }

}

int main(int argc, const char* argv[])
{
    const char *filename = argv[1];
    train(filename);
    return 0;
}
