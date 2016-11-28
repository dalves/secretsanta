#!/usr/bin/env python3
import hashlib
import random
from itertools import chain, combinations, product

TEMPLATE = """
<html>
<body style="font-size: 1.5em; background-image: url('snow.gif')">

<h2>
<img src="santa1.gif" />
2016 Secret Santa
<img src="santa2.gif" />
</h2>
<p>Ho ho ho! Hello there, <strong>{}</strong>! You are getting a gift for
<strong>{}</strong> in this year's secret santa.</p>
<p>Please try to stay under $30 and we'll look forward to seeing you on
Christmas Eve to exchange gifts and be merry!</p>
<p>Love,<br/>
Santa</p>
<p><small>P.S. the source code for this program is available
<a href="https://github.com/dalves/secretsanta">here</a></p>
</body>
</html>
"""

def branch_and_bound(N, all_edges):
    result = []

    def recurse(index, taken, givers, receivers):
        if result:
            return
        if len(givers) == N and len(receivers) == N:
            result.extend(taken)
            return
        if index >= len(all_edges):
            return
        giver, receiver = all_edges[index]

        if not (giver in givers) and not (receiver in receivers):
            recurse(
                    index + 1,
                    taken + [all_edges[index]],
                    givers | set([giver]),
                    receivers | set([receiver]))
        recurse(index + 1, taken, givers, receivers)

    recurse(0, [], set(), set())
    return result

SALT = input('Enter salt: ').strip()

def secret(string):
    return hashlib.sha1((SALT + string).encode('utf-8')).hexdigest()

def gen_edges(people, groups):
    disallowed = set()
    for g in groups:
        for p in g:
            disallowed.add((p, p))
        for a, b in combinations(g, 2):
            disallowed.add((a, b))
            disallowed.add((b, a))

    edges = [x for x in product(people, repeat=2) if x not in disallowed]
    return edges

def family():
    return [
        ['Brendan', 'Kristen', 'McCain', 'Evan'],
        ['Nancy', 'Zach', 'Veronica'],
        ['Ron', 'Jane'],
        ['Dave','Liz', 'Aria']
    ]


if __name__ == '__main__':

    people = list(chain.from_iterable(family()))
    edges = gen_edges(people, family())
    print(len(people), len(edges))

    random.shuffle(edges)

    assignments = branch_and_bound(len(people), edges)

    for giver, receiver in assignments:
        #print(giver, '-->', receiver)
        hashed_giver = secret(giver)
        with open(hashed_giver + '.html', 'w') as outfile:
            outfile.write(TEMPLATE.format(giver, receiver))
            outfile.close()
        print(giver + "'s assignment can be found at: " +
                "http://www.davidalves.net/santa/" + hashed_giver + ".html")

