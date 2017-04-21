import operator
import math
################ train and test files #############

train_file = open("data/train","r")
test_file = open("data/test","r")

###################################################

############### classify to spam or ham ##########

def classify(x,p,words_for_spam,words_for_ham):
    spam ,ham = p[0],p[1]
    o1,o2=math.log(spam),math.log(ham)
    w = x.split()
    for i in range(2, len(w), 2):
        o1 = o1 + int(w[i+1])*math.log(words_for_spam[w[i]])
        o2 = o2 + math.log(words_for_ham[w[i]])*int(w[i+1])
    if o1 > o2:
        return "spam"
    else:
        return "ham"

####################################################

########### initialize variables ##################

number_of_spams ,total = 0.0,0.0
words_for_spam = {}
words_for_ham ={}
total_words_of_spam = 0.0
total_words_of_ham = 0.0

##############################################

################## train #####################
for line in train_file:
    w = line.split()
    if w[1] == "spam":
        number_of_spams = number_of_spams + 1
        for x in range(2,len(w),2):
            total_words_of_spam += int(w[x+1])
            if w[x] in words_for_spam:
                words_for_spam[w[x]] += int(w[x+1])
            else:
                words_for_spam[w[x]] = int(w[x+1])
            if not (w[x] in words_for_ham):
                words_for_ham[w[x]]  = 0
    else:

        for x in range(2,len(w),2):
            total_words_of_ham += int(w[x + 1])
            if w[x] in words_for_ham:
                words_for_ham[w[x]] += int(w[x+1])
            else:
                words_for_ham[w[x]] = int(w[x+1])
            if not(w[x] in words_for_spam):
                words_for_spam[w[x]] = 0

    total = total + 1

######################################################

######################################################
pr_of_spam = ( number_of_spams + 1 ) / ( total + 2)
pr_of_ham = 1 - pr_of_spam

print "\nP(spam) = ",pr_of_spam
print "p(ham) = ",pr_of_ham

####################################################


words_for_spam.update((x, (y+1)/( total_words_of_spam + len(words_for_spam))) for x, y in words_for_spam.items())
words_for_ham.update((x, (y+1)/( total_words_of_ham + len(words_for_ham))) for x, y in words_for_ham.items())


################################################################################
def Get_accuracy(name_of_file,p,words_for_spam,words_for_ham):
    t = open(name_of_file, "r")
    total_number_of_testing_data = 0.0
    correct = 0.0
    for line in t:
        w = line.split()
        o = classify(line, p, words_for_spam, words_for_ham)
        if o == w[1]:
            correct += 1
        total_number_of_testing_data += 1
    accuracy = correct / total_number_of_testing_data
    t.close()
    return accuracy

###############################################################################
p = [pr_of_spam, pr_of_ham]

accuracy_of_train_data = Get_accuracy("data/train",p,words_for_spam,words_for_ham)
accuracy_of_test_data = Get_accuracy("data/test",p,words_for_spam,words_for_ham)

print "\nClassification error on training dataset = ", ( 1 - accuracy_of_train_data )*100 ,"%"
print  "Classification error on test dataset = " , (1 - accuracy_of_test_data )*100 ,"%"
words_for_spam = sorted(words_for_spam.items(), key=operator.itemgetter(1),reverse=True)
words_for_ham = sorted(words_for_ham.items(), key=operator.itemgetter(1),reverse=True)

print "\nMost words given spame are: "
print words_for_spam[0]
print words_for_spam[1]
print words_for_spam[2]
print words_for_spam[3]
print words_for_spam[4]

print "\nMost words given hme are: "
print words_for_ham[0]
print words_for_ham[1]
print words_for_ham[2]
print words_for_ham[3]
print words_for_ham[4]
