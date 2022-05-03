from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.

def backchain_to_goal_tree(rules, hypothesis):
    results = [hypothesis]
    for rule in rules:
        for consequent in rule.consequent():
            bindings = match(consequent, hypothesis)
            if bindings is not None:
                if isinstance(rule.antecedent(), str):
                    new_hypothesis = populate(rule.antecedent(), bindings)
                    results.append(backchain_to_goal_tree(rules, new_hypothesis))
                    results.append(new_hypothesis)
                else:
                    statements = [populate(antecedent, bindings) for antecedent in rule.antecedent()]
                    new_results = []
                    for statement in statements:
                        new_results.append(backchain_to_goal_tree(rules, statement))
                    if isinstance(rule.antecedent(), AND):
                        results.append(AND(new_results))
                    elif isinstance(rule.antecedent(), OR):
                        results.append(OR(new_results))
                    else:
                        results.append(new_results)
    return simplify(OR(results))

# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
