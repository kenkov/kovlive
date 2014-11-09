#! /usr/bin/env ruby
# coding:utf-8


include Math


def load_phrase_model(modelfile)
    phrasemodel = {}
    open modelfile do |file|
        while line = file.gets
            words, prob = line.split("\t")
            prob = prob.to_f
            w1, w2 = words.split(",")
            if not phrasemodel.has_key?(w1)
                phrasemodel[w1] = {}
            end
            phrasemodel[w1][w2] = prob
        end
    end
    return phrasemodel
end


def load_bigram_model(modelfile)
    unimodel = {}
    bimodel = {}
    open modelfile do |file|
        while line = file.gets
            words, prob = line.split("\t")
            prob = prob.to_f
            if words.include?(" ")
                w0, w1 = words.split(" ")
                bimodel[[w0, w1]] = prob
            else
                unimodel[words] = prob
            end
        end
    end
    return unimodel, bimodel
end


def bigram_prob(
        w0, w1, unimodel, bimodel,
        lambda2: 0.95,
        lambda1: 0.95,
        unk_n: 1e6
)
    if bimodel.has_key? [w0, w1]
        prob = lambda2 * bimodel[[w0, w1]]
    elsif unimodel.has_key? w1
        prob = (1 - lambda2) * lambda1 * unimodel[w1]
    else
        prob = (1 - lambda2) * (1 - lambda1) * (1.0 / unk_n)
    end
    return - Math.log(prob)
end


def phrase_prob(
    p1, p2, phrasemodel,
    lambda1: 0.95,
    unk_n: 1e6
)
    if phrasemodel.has_key? p1 and phrasemodel[p1].has_key? p2
        prob = lambda1 * phrasemodel[p1][p2]
    else
        prob = (1 - lambda1) * (1.0 / unk_n)
    end
    puts "#{p1} #{p2} #{prob}"
    return - Math.log(prob)
end


def _search(
        sent_without_symbol,
        unimodel,
        bimodel,
        phrasemodel,
        start_symbol: '<s>',
        end_symbol: '</s>',
        max_len: 100,
        verbose: false
)
    sent = [start_symbol] + sent_without_symbol + [end_symbol]
    sent_len = sent.length
    best = (0...sent_len).map { |_| {} }
    best[0][ [start_symbol, [0, 0]] ] = 0.0
    before_pos = (0...sent_len).map { |_| {} }

    (0...sent_len-1).each do |curpos|
        next_start = curpos + 1
        (next_start...[sent_len, next_start+max_len].min).each do |next_end|
            next_phrase = sent[next_start, next_end+1-next_start].join("")
            next_word = sent[next_start]
            best[curpos].each do |cur_key, prob|
                cur_phrase = cur_key[0]
                #cur_start = cur_key[1][0]
                #cur_end = cur_key[1][1]
                conv_w0 = cur_phrase[-1]

                if next_start == next_end and \
                        ((not phrasemodel.has_key? next_phrase) \
                         or (not phrasemodel[next_phrase].has_key? next_word))
                    #
                    # WRITE conversion from fullwidth-katakana to halfwidth-katakana
                    conv_phrase = next_phrase
                    #
                    conv_w1 = conv_phrase[0]
                    next_key = [conv_phrase, [next_start, next_end]]
                    next_prob = prob \
                        + bigram_prob(
                            conv_w0,
                            conv_w1,
                            unimodel,
                            bimodel) \
                        + phrase_prob(
                            next_phrase,
                            next_word,
                            phrasemodel)
                    if best[next_end].has_key? next_key
                        if best[next_end][next_key] >= next_prob
                            best[next_end][next_key] = next_prob
                            before_pos[next_end][next_key] = cur_key
                        end
                    else
                        best[next_end][next_key] = next_prob
                        before_pos[next_end][next_key] = cur_key
                    end
                end
                if phrasemodel.has_key? next_phrase
                    phrasemodel[next_phrase].keys.each do |conv_phrase|
                        conv_w1 = conv_phrase[0]
                        next_key = [conv_phrase, [next_start, next_end]]
                        next_prob = prob \
                            + bigram_prob(
                                conv_w0,
                                conv_w1,
                                unimodel,
                                bimodel) \
                            + phrase_prob(
                                next_phrase,
                                conv_phrase,
                                phrasemodel)
                        if best[next_end].has_key? next_key
                            if best[next_end][next_key] >= next_prob
                                best[next_end][next_key] = next_prob
                                before_pos[next_end][next_key] = cur_key
                            end
                        else
                            best[next_end][next_key] = next_prob
                            before_pos[next_end][next_key] = cur_key
                        end
                    end
                end
            end
        end
    end

    ans = []
    ind = sent_len - 1
    start = ind
    ed = ind
    min_val = Float::INFINITY
    min_key = ""
    best[ind].each do |best_key, val|
        key = best_key[0]
        if min_val > val
            min_key = key
            min_val = val
        end
    end
    ans.push(min_key)
    phrase, index_pair = before_pos[ind][[min_key, [start, ed]]]
    start = index_pair[0]
    ed = index_pair[1]
    ans.push(phrase)

    while ed != 0
        phrase, index_pair = before_pos[ed][[phrase, [start, ed]]]
        start = index_pair[0]
        ed = index_pair[1]
        ans.push(phrase)
    end

    ans.reverse!

    p best
    p before_pos
    return ans
end


def search(
        sent_without_symbol,
        unimodel,
        bimodel,
        phrasemodel,
        start_symbol: '<s>',
        end_symbol: '</s>',
        max_len: 100,
        verbose: false
)
    ans = _search(
        sent_without_symbol.split(""),
        unimodel,
        bimodel,
        phrasemodel)
    return ans.join('').gsub(/(^\<s\>|\<\/s\>$)/, "")
end


phrasemodel = load_phrase_model("phrase.model")
unimodel, bimodel = load_bigram_model("bigram.model")
text = "今日は、ステーキを食べに出掛けます。"
puts search(text, unimodel, bimodel, phrasemodel)
