states = ('Zdravá', 'Nemocná')

observations = ('výborně', 'slabě', 'na umření')

start_probability = {'Zdravá': 0.6, 'Nemocná': 0.4}

transition_probability = {
    'Zdravá': {'Zdravá': 0.7, 'Nemocná': 0.3},
    'Nemocná': {'Zdravá': 0.4, 'Nemocná': 0.6},
}

emission_probability = {
    'Zdravá': {'výborně': 0.5, 'slabě': 0.4, 'na umření': 0.1},
    'Nemocná': {'výborně': 0.1, 'slabě': 0.3, 'na umření': 0.6},
}


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]
    path = {}

    # Initialize base cases (t == 0)
    for y in states:
        V[0][y] = start_p[y] * emit_p[y][obs[0]]
        path[y] = [y]

    # Run Viterbi for t > 0
    for t in range(1,len(obs)):
        V.append({})
        newpath = {}

        for y in states:
            (prob, state) = max([(V[t-1][y0] * trans_p[y0][y] * emit_p[y][obs[t]], y0) for y0 in states])
            V[t][y] = prob
            newpath[y] = path[state] + [y]

        # Don't need to remember the old paths
        path = newpath

    (prob, state) = max([(V[len(obs) - 1][y], y) for y in states])
    return (prob, path[state])

res = viterbi(observations,
                   states,
                   start_probability,
                   transition_probability,
                   emission_probability)

print()