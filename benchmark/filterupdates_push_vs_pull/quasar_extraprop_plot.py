# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt  # pip install matplotlib
import json


push_x = []
push_y_success = []
push_y_redundant = []
push_y_spam = []
pull_x = []
pull_y_success = []
pull_y_redundant = []
pull_y_spam = []


pull_samples = [
    json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_a.json", "r")),  # NOQA
    json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_b.json", "r")),  # NOQA
    json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_c.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_d.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_e.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_f.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_g.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_h.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_pull_i.json", "r")),  # NOQA
]

push_samples = [
    json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_a.json", "r")),  # NOQA
    json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_b.json", "r")),  # NOQA
    json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_c.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_d.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_e.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_f.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_g.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_h.json", "r")),  # NOQA
#   json.load(open("benchmark/filterupdates_push_vs_pull/quasar_extraprop_push_i.json", "r")),  # NOQA
]


for sample in push_samples:
    push_x.append(sample["quasar"]["constants"]["extra_propagations"])
    success = sample["quasar"]["update_successful"]
    redundant = sample["quasar"]["update_redundant"]
    spam = sample["quasar"]["update_spam"]
    push_y_success.append(redundant + spam + success)
    push_y_redundant.append(redundant + spam)
    push_y_spam.append(spam)


for sample in pull_samples:
    pull_x.append(sample["quasar"]["constants"]["extra_propagations"])
    success = sample["quasar"]["update_successful"]
    redundant = sample["quasar"]["update_redundant"]
    spam = sample["quasar"]["update_spam"]
    pull_y_success.append(redundant + spam + success)
    pull_y_redundant.append(redundant + spam)
    pull_y_spam.append(spam)


# setup
fig = plt.figure()
plot = fig.add_subplot(111)
plot.set_xlabel('Extra propagations')
plot.set_ylabel('Update calls')
# plot.set_xscale('log')
# plot.set_yscale('log')
plot.axis([0, 16, 0, 400000])


# pull plots
lines = plot.plot(pull_x, pull_y_success, 'k', label='Pull success')
plt.setp(lines, color='#FFAAAA', linewidth=2.0)
# plot.fill_between(pull_x, pull_y_redundant, pull_y_success,
#                   facecolor="#00FF00", alpha=0.5)

lines = plot.plot(pull_x, pull_y_redundant, 'k', label='Pull redundant')
plt.setp(lines, color='#FF5555', linewidth=2.0)
# plot.fill_between(pull_x, pull_y_spam, pull_y_redundant,
#                   facecolor="#FFFF00", alpha=0.5)

lines = plot.plot(pull_x, pull_y_spam, 'k', label='Pull spam')
plt.setp(lines, color='#FF0000', linewidth=2.0)
# plot.fill_between(pull_x, 0, pull_y_spam, facecolor="#FF0000", alpha=0.5)


# push plots
lines = plot.plot(push_x, push_y_success, 'k', label='Push success')
plt.setp(lines, color='#AAAAFF', linewidth=2.0)
# plot.fill_between(push_x, push_y_redundant, push_y_success,
#                   facecolor="#00FF00", alpha=0.5)

lines = plot.plot(push_x, push_y_redundant, 'k', label='Push redundant')
plt.setp(lines, color='#5555FF', linewidth=2.0)
# plot.fill_between(push_x, push_y_spam, push_y_redundant,
#                   facecolor="#FFFF00", alpha=0.5)

lines = plot.plot(push_x, push_y_spam, 'k', label='Push spam')
plt.setp(lines, color='#0000FF', linewidth=2.0)
# plot.fill_between(push_x, 0, push_y_spam, facecolor="#FF0000", alpha=0.5)


# create legend
plot = plot.legend(loc='upper center', shadow=False, fontsize='small')
plot.get_frame().set_facecolor('#00FFFF')


# render
plt.savefig("benchmark/filterupdates_push_vs_pull/quasar_extraprop_plot.png")
plt.show()
