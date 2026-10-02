
def calculate(expences):
    persons = {}
    debtors = []
    creditors = []

    for expense in expences:

        payer = expense["payer"]
        
        if payer not in persons:
             persons[payer] = 0.0
        persons[payer] += expense["total_amount"]

        for borrower in expense["borrowers"]:
            name = borrower["name"]

            if name not in persons:
                persons[name] = 0.0

            persons[name] -= borrower["owes"]

        ListOfKeys = list(persons.keys())

    for i in range(len(ListOfKeys)):
        if persons[ListOfKeys[i]] < 0:
            debtors+=[[ListOfKeys[i],persons[ListOfKeys[i]]]]
        if persons[ListOfKeys[i]] > 0:
            creditors+=[[ListOfKeys[i],persons[ListOfKeys[i]]]]
            
    return (debtors,creditors)

def solve(debtors,creditors):

    s_debtors = sorted(debtors, key = lambda x: x[1])
    s_creditors = sorted(creditors, key = lambda x: x[1], reverse=True)

    transfers = []

    while len(s_debtors) > 0 and len(s_creditors) > 0:
        
        if abs(s_debtors[0][1]) <= abs(s_creditors[0][1]):
            transfers+=[(s_debtors[0][0],s_creditors[0][0],abs(s_debtors[0][1]))]
            s_creditors[0][1] -= abs(s_debtors[0][1])
            s_debtors.remove(s_debtors[0])
            s_creditors =  sorted(s_creditors, key = lambda x: x[1], reverse=True)
        else:
            transfers+=[(s_debtors[0][0],s_creditors[0][0],abs(s_creditors[0][1]))]
            s_debtors[0][1] += s_creditors[0][1]
            s_creditors.remove(s_creditors[0])
            s_debtors =  sorted(s_debtors, key = lambda x: x[1])

    return transfers


    




