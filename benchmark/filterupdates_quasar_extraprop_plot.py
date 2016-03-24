# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt  # pip install matplotlib
import json


x = []
y_success = []
y_redundant = []
y_spam = []


samples = [
    json.load(open("benchmark/filterupdates_quasar_extraprop_a.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_b.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_c.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_d.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_e.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_f.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_g.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_h.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_i.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_j.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_k.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_l.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_m.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_n.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_o.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_p.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_extraprop_q.json", "r")),
]


for sample in samples:
    x.append(sample["quasar"]["constants"]["extra_propagations"])
    success = sample["quasar"]["update_successful"]
    redundant = sample["quasar"]["update_redundant"]
    spam = sample["quasar"]["update_spam"]
    y_success.append(redundant + spam + success)
    y_redundant.append(redundant + spam)
    y_spam.append(spam)


# setup
fig = plt.figure()
plot = fig.add_subplot(111)
plot.set_xlabel('Extra propagations')
plot.set_ylabel('Update calls')
# plot.set_xscale('log')
# plot.set_yscale('log')
plot.axis([0, 16, 0, 250000])


# add plots
lines = plot.plot(x, y_success, 'k', label='Success')
plt.setp(lines, color='green', linewidth=2.0)
plot.fill_between(x, y_redundant, y_success, facecolor="#00FF00", alpha=0.5)

lines = plot.plot(x, y_redundant, 'k', label='Redundant')
plt.setp(lines, color='orange', linewidth=2.0)
plot.fill_between(x, y_spam, y_redundant, facecolor="#FFFF00", alpha=0.5)

lines = plot.plot(x, y_spam, 'k', label='Spam')
plt.setp(lines, color='red', linewidth=2.0)
plot.fill_between(x, 0, y_spam, facecolor="#FF0000", alpha=0.5)


# create legend
plot = plot.legend(loc='upper center', shadow=False, fontsize='small')
plot.get_frame().set_facecolor('#00FFFF')


# render
plt.savefig("benchmark/filterupdates_quasar_extraprop_plot.png")
plt.show()
