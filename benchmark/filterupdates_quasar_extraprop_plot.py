# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt  # pip install matplotlib
import json


x_success = []
y_success = []
x_redundant = []
y_redundant = []
x_spam = []
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
    extra_propagations = sample["quasar"]["constants"]["extra_propagations"]
    x_success.append(extra_propagations)
    y_success.append(sample["quasar"]["update_successful"])
    x_redundant.append(extra_propagations)
    y_redundant.append(sample["quasar"]["update_redundant"])
    x_spam.append(extra_propagations)
    y_spam.append(sample["quasar"]["update_spam"])


# setup
fig = plt.figure()
plot = fig.add_subplot(111)
plot.set_xlabel('Extra propagations')
plot.set_ylabel('Update calls')
# plot.set_xscale('log')
# plot.set_yscale('log')
# plot.axis([0, 20, 0, 100])

# add plots
lines = plot.plot(x_success, y_success, 'k', label='Success')
plt.setp(lines, color='green', linewidth=2.0)
lines = plot.plot(x_redundant, y_redundant, 'k', label='Redundant')
plt.setp(lines, color='orange', linewidth=2.0)
lines = plot.plot(x_spam, y_spam, 'k', label='Spam')
plt.setp(lines, color='red', linewidth=2.0)

# create legend
plot = plot.legend(loc='upper center', shadow=False, fontsize='small')
plot.get_frame().set_facecolor('#00FFFF')


# render
plt.savefig("benchmark/filterupdates_quasar_extraprop_plot.png")
