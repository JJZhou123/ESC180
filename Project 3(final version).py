
def cosine_similarity(vec1, vec2):
    numerator = 0
    denominator1 = 0
    denominator2 = 0
    denominator = 0

    for i in vec1:
        for a in vec2:
            if i == a:
                numerator += vec1[i] * vec2[i]

    for i in vec1:
        denominator1 += vec1[i]**2
    for i in vec2:
        denominator2 += vec2[i]**2
    denominator = (denominator1*denominator2)**0.5

    return numerator/denominator



def build_semantic_descriptors(sentences):
    dic = {}
    # n/15 sentences in total
    # run time = n/15 * (C = 15+15!) = n*15!
    # run time O(15!*n)
    for sentence in sentences: ### n/15 assume 15 words in one sentence


    # complexity under this for loop is 15 + 15! = C for one sentence

        shorten = []
        for word in sentence: ### 15

            if word not in shorten:
                shorten.append(word)
            if word not in dic:
                dic.update({word:{}})

        temp = shorten
        index = 0

        # this part is 15*14! = 15!
        for word in shorten: ### 15
            index += 1
            for temp_word in temp[index:]: ### 14-13-12-11 ...0
                    if word not in dic[temp_word]:
                        dic[temp_word].update({word: 0})
                    if temp_word not in dic[word]:
                        dic[word].update({temp_word: 0})
                    dic[word].update({temp_word: 1 + dic[word][temp_word]})
                    dic[temp_word].update({word: 1 + dic[temp_word][word]})


    return dic

def build_semantic_descriptors_from_files(filenames):

    sentences = []

    for i in range(0, len(filenames)):
        f = open(filenames[i], "r", encoding = "utf-8-sig")
        whole_book = f.readlines()
        txt = ""

        for i in whole_book:
            sentence = i.rstrip()
            txt += sentence + " "


        txt = txt.lower()

        txt =txt.replace(", ", "+")
        txt =txt.replace("-", "+")
        txt =txt.replace("--", "+")
        txt =txt.replace("; ", "+")
        txt =txt.replace(": ", "+")
        txt =txt.replace(",", "+")
        # txt = txt.replace("â€”", "+")
        txt =txt.replace(";", "+")
        txt =txt.replace(":", "+")
        # txt = txt.replace("*", "+")
        # txt = txt.replace("(", "+")
        # txt = txt.replace(")", "+")
        # txt = txt.replace(" \"", "+")
        # txt = txt.replace("\' s ", "+")
        # txt = txt.replace("\'", "+")
        # txt = txt.replace(" (", "+")
        # txt = txt.replace(") ", "+")
        txt = txt.replace(" \"", "+")
        txt = txt.replace(", \"", "+")
        txt = txt.replace("?\"+", "+")
        txt = txt.replace("!\"+", "+")
        txt = txt.replace(".\"+", "+")
        txt = txt.replace("?\â€+", "+")
        txt = txt.replace("!\â€+", "+")
        txt = txt.replace(".\â€+", "+")
        txt = txt.replace("?\"", "+")
        txt = txt.replace("!\"", "+")
        txt = txt.replace(".\"", "+")
        txt = txt.replace("?\â€", "+")
        txt = txt.replace("!\â€", "+")
        txt = txt.replace(".\â€", "+")
        txt = txt.replace(" ", "+")
        txt = txt.replace("...+", " ")
        txt = txt.replace("!!!+", " ")
        txt = txt.replace("???+", " ")
        txt =txt.replace(".+", " ")
        txt =txt.replace("?+", " ")
        txt =txt.replace("!+", " ")
        txt = txt.split()

        for sentence in txt:
            sentence = sentence.replace("+", " ")
            sentence = sentence.split()
            sentences.append(sentence)


    sem_des = build_semantic_descriptors(sentences)
    return sem_des

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):

    cur_sim = -2

    for choice in choices:

        prev_sim = cur_sim

        if choice not in semantic_descriptors:
            cur_sim = -1
        if choice in semantic_descriptors:
            vec1 = semantic_descriptors[word]
            vec2 = semantic_descriptors[choice]
            if vec1 == {} or vec2 == {}:
                cur_sim = -1
            if vec1 != {} and vec2 != {}:
                cur_sim = similarity_fn(vec1, vec2)


        cur_sim = max(cur_sim, prev_sim)

        if cur_sim > prev_sim:
            ans = choice

    return ans

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    test = open(filename, "r", encoding = "latin1")
    test = test.readlines()
    test1 = []
    correct = 0
    for line in test:
        option = line.split()
        test1.append(option)

    for line in test1:
        choices = line[2:]
        guess = most_similar_word(line[0], choices, semantic_descriptors, similarity_fn)
        if guess == line[1] :
            correct += 1

    percentage = 100 * correct/len(test1)
    return percentage



if __name__ == "__main__":
    # print(cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))

    # build_semantic_descriptors_from_files(filenames)
    #
    # most_similar_word(word, choices, semantic_descriptors, cosine_similarity)
    # vec1 = {"i": 3, "am": 3, "a": 2, "sick": 1, "spiteful": 1, "an": 1, "unattractive": 1}
    # vec2 = {"i": 1, "believe": 1, "my": 1, "is": 1, "diseased": 1}
    #
    # cosine_similarity(vec1, vec2)
    # {'monkey': {'apple': 3, 'banana': 2, 'orange': 1}, 'apple': {'monkey': 3, 'banana': 2, 'orange': 1}, 'banana': {'monkey': 2, 'apple': 2, 'orange': 1}, 'orange': {'monkey': 1, 'banana': 1, 'apple': 1}}
    #
    #
    # vec1 =  {'apple': 3, 'banana': 2, 'orange': 1} # monkey
    #
    #
    # vec2 = {'monkey': 3, 'banana': 2, 'orange': 1} # 'apple'
    #
    # cosine_similarity(vec1, vec2)
    # word = "monkey"
    # choices = ["apple", "banana"]
    # files = ["day1.txt"]
    #
    #
    # semantic_descriptors = build_semantic_descriptors_from_files(files)

    # most_similar_word(word, choices, semantic_descriptors, cosine_similarity)
    word = "dog"
    choices = ["cat", "rat"]
    sem_desc = {"dog": {"cat": 1, "food": 1},"cat": {"dog": 1}}

    most_similar_word("dog",choices, sem_desc,cosine_similarity)

    #
    #
    # filenames = ["HarryPotter.txt"]
    # #
    # semantic_descriptors = build_semantic_descriptors_from_files(filenames)
    # #
    # run_similarity_test("text.txt", semantic_descriptors, cosine_similarity)
    # # # # #
    # # # #