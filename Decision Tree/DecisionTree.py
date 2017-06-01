from math import log

class Node:
  """
  A simple node class to build our tree with. It has the following:
  
  children (dictionary<str,Node>): A mapping from attribute value to a child node
  attr (str): The name of the attribute this node classifies by. 
  islead (boolean): whether this is a leaf. False.
  """
  
  def __init__(self,attr):
    self.children = {}
    self.attr = attr
    self.isleaf = False

class LeafNode(Node):
    """
    A basic extension of the Node class with just a value.
    
    value (str): Since this is a leaf node, a final value for the label.
    islead (boolean): whether this is a leaf. True.
    """
    def __init__(self,value):
        self.value = value
        self.isleaf = True
    
class Tree:
  """
  A generic tree implementation with which to implement decision tree learning.
  Stores the root Node and nothing more. A nice printing method is provided, and
  the function to classify values is left to fill in.
  """
  def __init__(self, root=None):
    self.root = root

  def prettyPrint(self):
    print str(self)
    
  def preorder(self,depth,node):
    if node is None:
      return '|---'*depth+str(None)+'\n'
    if node.isleaf:
      return '|---'*depth+str(node.value)+'\n'
    string = ''
    for val in node.children.keys():
      childStr = '|---'*depth
      childStr += '%s = %s'%(str(node.attr),str(val))
      string+=str(childStr)+"\n"+self.preorder(depth+1, node.children[val])
    return string    

  def count(self,node=None):
    if node is None:
      node = self.root
    if node.isleaf:
      return 1
    count = 1
    for child in node.children.values():
      if child is not None:
        count+= self.count(child)
    return count  

  def __str__(self):
    return self.preorder(0, self.root)

  def classifyHelper(self, classificationData, curNode):
    # if the node is a leaf node:
    # return the classification
    if curNode.isleaf:
        return curNode.value

        # set Node = child of the current Node that has the value of the attribute at that node from the classification data
    else:
        curAttr = curNode.attr
        childVal = classificationData[curAttr]
        newNode = curNode.children[childVal]
        return self.classifyHelper(classificationData, newNode)
  
  def classify(self, classificationData):
    """
    Uses the classification tree with the passed in classificationData.`
    
    Args:
        classificationData (dictionary<string,string>): dictionary of attribute values
    Returns:
        str
        The classification made with this tree.
    """
    #YOUR CODE HERE
    return self.classifyHelper(classificationData, self.root)


  
def getPertinentExamples(examples,attrName,attrValue):
    """
    Helper function to get a subset of a set of examples for a particular assignment 
    of a single attribute. That is, this gets the list of examples that have the value 
    attrValue for the attribute with the name attrName.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValue (str): a value of the attribute
    Returns:
        list<dictionary<str,str>>
        The new list of examples.
    """
    newExamples = []
    #YOUR CODE HERE
    for example in examples:
        for key, value in example.iteritems():
            # print key
            # print value
            if key == attrName and value == attrValue:
                newExamples.append(example)
    return newExamples
  
def getClassCounts(examples,className):
    """
    Helper function to get a dictionary of counts of different class values
    in a set of examples. That is, this returns a dictionary where each key 
    in the list corresponds to a possible value of the class and the value
    at that key corresponds to how many times that value of the class 
    occurs.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        className (str): the name of the class
    Returns:
        dictionary<string,int>
        This is a dictionary that for each value of the class has the count
        of that class value in the examples. That is, it maps the class value
        to its count.
    """
    classCounts = {}

    #YOUR CODE HERE
    for example in examples:
        for key, value in example.iteritems():
            if key == className:
                if value not in classCounts:
                    classCounts[value] = 1
                else:
                    classCounts[value] += 1


    return classCounts

def getMostCommonClass(examples,className):
    """
    A freebie function useful later in makeSubtrees. Gets the most common class
    in the examples. See parameters in getClassCounts.
    """
    counts = getClassCounts(examples,className)
    return max(counts, key=counts.get) if len(examples)>0 else None

def getAttributeCounts(examples,attrName,attrValues,className):
    """
    Helper function to get a dictionary of counts of different class values
    corresponding to every possible assignment of the passed in attribute. 
	  That is, this returns a dictionary of dictionaries, where each key  
	  corresponds to a possible value of the attribute named attrName and holds
 	  the counts of different class values for the subset of the examples
 	  that have that assignment of that attribute.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<str>): list of possible values for the attribute
        className (str): the name of the class
    Returns:
        dictionary<str,dictionary<str,int>>
        This is a dictionary that for each value of the attribute has a
        dictionary from class values to class counts, as in getClassCounts
    """
    attributeCounts={}
    #YOUR CODE HERE

    #loop through examples
    #add key to outer dictionary for each possible assignment of the given attribute
    #get subset of examples that have the assignment of the given attribute
    #for each example, calculate counts of possible class values

    for val in attrValues:
        myDict = {}
        for example in examples:
            for key, value in example.iteritems():
                if key == attrName and value == val:
                    classVal = example[className]
                    if classVal not in myDict:
                        myDict[classVal] = 1
                    else:
                        myDict[classVal] += 1
        attributeCounts[val] = myDict

    return attributeCounts
        

def setEntropy(classCounts):
    """
    Calculates the set entropy value for the given list of class counts.
    This is called H in the book. Note that our labels are not binary,
    so the equations in the book need to be modified accordingly. Note
    that H is written in terms of B, and B is written with the assumption 
    of a binary value. B can easily be modified for a non binary class
    by writing it as a summation over a list of ratios, which is what
    you need to implement.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The set entropy score of this list of class value counts.
    """
    #YOUR CODE HERE
    import math

    denom = 0.0
    for count in classCounts:
        denom += count

    entropy = 0.0
    for count in classCounts:
        q = count/denom
        add = q *  math.log(q, 2)
        entropy += add

    entropy = -1.0*entropy
    return entropy



def remainder(examples,attrName,attrValues,className):
    """
    Calculates the remainder value for given attribute and set of examples.
    See the book for the meaning of the remainder in the context of info 
    gain.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The remainder score of this value assignment of the attribute.
    """
    #YOUR CODE HERE

    totalEx = float(len(examples))
    remainder = 0.0

    for value in attrValues:
        #get the subset of examples that have that value of that attribute using get pertinent examples
        subset = getPertinentExamples(examples, attrName, value)

        # call getClassCounts on that subset of examples
        myCounts = getClassCounts(subset, className)

        #call setEntropy on the classCounts to get the RHS
        entropy = setEntropy(dict.values(myCounts))

        #multiply by (total number of examples in getPertinentExamples)/totalEx
        mult = len(subset)/totalEx

        #sum the values
        remainder += mult*entropy
    return remainder


          
def infoGain(examples,attrName,attrValues,className):
    """
    Calculates the info gain value for given attribute and set of examples.
    See the book for the equation - it's a combination of setEntropy and
    remainder (setEntropy replaces B as it is used in the book).
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get remainder for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The gain score of this value assignment of the attribute.
    """
    #YOUR CODE HERE
    myCounts = getClassCounts(examples, className)
    myCounts = dict.values(myCounts)
    entropy = setEntropy(myCounts)

    myRemainder = remainder(examples, attrName, attrValues, className)
    return entropy - myRemainder

  
def giniIndex(classCounts):
    """
    Calculates the gini value for the given list of class counts.
    See equation in instructions.
    
    Args:
        classCounts (list<int>): list of counts of each class value
    Returns:
        float
        The gini score of this list of class value counts.
    """
    #YOUR CODE HERE

    total = float(sum(classCounts))
    mySum = 0.0

    for count in classCounts:
        p = count/total
        p2 = p*p
        mySum += p2

    return 1 - mySum


    #for count in classCounts:
        #calculate p^2: divide class count by total and square
        #add it to the sum
    #return 1 - the sum

    #get p (relative frequency) by summing the list and then dividing each frequency by the total


  
def giniGain(examples,attrName,attrValues,className):
    """
    Return the inverse of the giniD function described in the instructions.
    The inverse is returned so as to have the highest value correspond 
    to the highest information gain as in entropyGain. If the sum is 0,
    return sys.maxint.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrName (str): the name of the attribute to get counts for
        attrValues (list<string>): list of possible values for attribute
        className (str): the name of the class
    Returns:
        float
        The summed gini index score of this list of class value counts.
    """
    #YOUR CODE HERE
    #loop through attrValues
        #call getPertinentExamples
        #get the classCounts (?)
        #calculate the gini index for each one
    import sys
    giniD = 0.0

    for value in attrValues:
        pertinentExamples = getPertinentExamples(examples, attrName, value)
        myClassCounts = getClassCounts(pertinentExamples, className)
        myClassCounts = dict.values(myClassCounts)
        curGini = giniIndex(myClassCounts)
        mult = float(len(pertinentExamples))/float(len(examples))
        add = curGini * mult
        giniD += add

    if giniD == 0.0:
        return sys.maxint

    return 1/giniD



    
def makeTree(examples, attrValues,className,setScoreFunc,gainFunc):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makeSubtrees(remainingAttributes,examples,attrValues,className,getMostCommonClass(examples,className),setScoreFunc,gainFunc))
    
def makeSubtrees(remainingAttributes,examples,attributeValues,className,defaultLabel,setScoreFunc,gainFunc):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE

    #if examples is empty then return default
    if len(examples) == 0:
        return LeafNode(defaultLabel)

    # if all examples have the same classification then return classification
    # loop through each example
    # get its class label and compare it to the class label of the previous example
    # update the flag accordingly
    different = False
    counter = 0
    curLabel = examples[0][className]
    while different == False and counter < len(examples) - 1:
        ex = examples[counter]
        curLabel = ex[className]
        nextEx = examples[counter+1]
        nextLabel = nextEx[className]
        if curLabel != nextLabel:
            different = True
        counter = counter + 1

    if different == False:
        return LeafNode(curLabel)

    #JUST USE CLASS COUNTS HERE

    #get the most common value using getMostCommonClass
    if len(remainingAttributes) == 0:
        myClass = getMostCommonClass(examples, className)
        return LeafNode(myClass)

    else:
        # calculate gainFunc for each--pass in attrValues, className, and examples
        import sys
        max = -sys.maxint - 1
        maxAttr = None
        for attribute in remainingAttributes:
            gain = gainFunc(examples, attribute, attributeValues[attribute], className)
            if gain > max:
                max = gain
                maxAttr = attribute

        # pick the attribute with the maximum information gain
        #create new tree with the best attribute as the root

        myTree = Node(maxAttr)



        #m = majority-values(examples)
        m = getMostCommonClass(examples, className)

        for value in attributeValues[maxAttr]:
            relevantEx = getPertinentExamples(examples, maxAttr, value)

            #IF NO PERTINENT EXAMPLES, APPEND A LEAF NODE
            if len(relevantEx) == 0:
                myTree.children[value] = LeafNode(m)
            else:

                #    remainingAttributes.remove(maxAttr)
                if maxAttr in remainingAttributes:
                    newAttributes = list(remainingAttributes)
                    newAttributes.remove(maxAttr)
                myTree.children[value] = makeSubtrees(newAttributes, relevantEx, attributeValues,className,defaultLabel,setScoreFunc,gainFunc)

        return myTree






def makePrunedTree(examples, attrValues,className,setScoreFunc,gainFunc,q):
    """
    Creates the classification tree for the given examples. Note that this is implemented - you
    just need to imeplement makeSubtrees.
    
    Args:
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        classScoreFunc (func): the function to score classes (ie setEntropy or giniIndex)
        gainFunc (func): the function to score gain of attributes (ie infoGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Tree
        The classification tree for this set of examples
    """
    remainingAttributes=attrValues.keys()
    return Tree(makePrunedSubtrees(remainingAttributes,examples,attrValues,className,getMostCommonClass(examples,className),setScoreFunc,gainFunc,q))
    
def makePrunedSubtrees(remainingAttributes,examples,attributeValues,className,defaultLabel,setScoreFunc,gainFunc,q):
    """
    Creates a classification tree Node and all its children. This returns a Node, which is the root
    Node of the tree constructed from the passed in parameters. This should be implemented recursively,
    and handle base cases for zero examples or remainingAttributes as covered in the book.    

    Args:
        remainingAttributes (list<string>): the names of attributes still not used
        examples (list<dictionary<str,str>>): list of examples
        attrValues (dictionary<string,list<string>>): list of possible values for attribute
        className (str): the name of the class
        defaultLabel (string): the default label
        setScoreFunc (func): the function to score classes (ie classEntropy or gini)
        gainFunc (func): the function to score gain of attributes (ie entropyGain or giniGain)
        q (float): the Chi-Squared pruning parameter
    Returns:
        Node or LeafNode
        The classification tree node optimal for the remaining set of attributes.
    """
    #YOUR CODE HERE (Extra Credit)
    #if examples is empty then return default

    from scipy.stats.stats import chisqprob

    if len(examples) == 0:
        return LeafNode(defaultLabel)

    # if all examples have the same classification then return classification
    # loop through each example
    # get its class label and compare it to the class label of the previous example
    # update the flag accordingly
    different = False
    counter = 0
    curLabel = examples[0][className]
    while different == False and counter < len(examples) - 1:
        ex = examples[counter]
        curLabel = ex[className]
        nextEx = examples[counter+1]
        nextLabel = nextEx[className]
        if curLabel != nextLabel:
            different = True
        counter = counter + 1

    if different == False:
        return LeafNode(curLabel)

    #JUST USE CLASS COUNTS HERE

    #get the most common value using getMostCommonClass
    if len(remainingAttributes) == 0:
        myClass = getMostCommonClass(examples, className)
        return LeafNode(myClass)

    else:
        # calculate gainFunc for each--pass in attrValues, className, and examples
        import sys
        max = -sys.maxint - 1
        maxAttr = None
        for attribute in remainingAttributes:
            gain = gainFunc(examples, attribute, attributeValues[attribute], className)
            if gain > max:
                max = gain
                maxAttr = attribute


        #magnitude of D = number of relevant examples?
        #implement chi-squared pruning here?

        devX = 0 #SEE BELOW--NOT SURE HOW TO CALCULATE THIS
        for i in range(0, len(attributeValues[maxAttr])):
            #note: class counts returns a dictionary of class counts
            classCounts = getClassCounts(maxAttr)


            currentVal = attributeValues[maxAttr][i]
            relEx = getPertinentExamples(examples, maxAttr, currentVal)
            #pn =

            #use class counts to get the "positive" and "negative" examples



        p = chisqprob(devX)
        v = len(attributeValues[maxAttr])
        if p > q:
            print "p > q"

            #return

        #get dev(X): is this just the chi-squared statistic for
            #for i in range (0,number of values of attribute X):
                #get px and nx (how?)
                #get px-hat and nx-hat (how?)
                #px-hat = ?
                #where does D come from? What do the absolute value bars around D mean?


        # pick the attribute with the maximum information gain
        #create new tree with the best attribute as the root

        myTree = Node(maxAttr)



        #m = majority-values(examples)
        m = getMostCommonClass(examples, className)

        for value in attributeValues[maxAttr]:
            relevantEx = getPertinentExamples(examples, maxAttr, value)

            #IF NO PERTINENT EXAMPLES, APPEND A LEAF NODE
            if len(relevantEx) == 0:
                myTree.children[value] = LeafNode(m)
            else:

                #    remainingAttributes.remove(maxAttr)
                if maxAttr in remainingAttributes:
                    newAttributes = list(remainingAttributes)
                    newAttributes.remove(maxAttr)
                myTree.children[value] = makeSubtrees(newAttributes, relevantEx, attributeValues,className,defaultLabel,setScoreFunc,gainFunc)

        return myTree

