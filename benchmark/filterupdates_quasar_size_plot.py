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
    json.load(open("benchmark/filterupdates_quasar_size_a.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_b.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_c.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_d.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_e.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_f.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_g.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_h.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_i.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_size_j.json", "r")),
]


for sample in samples:
    quasar_size = sample["quasar"]["constants"]["size"]
    x_success.append(quasar_size)
    y_success.append(sample["quasar"]["update_successful"])
    x_redundant.append(quasar_size)
    y_redundant.append(sample["quasar"]["update_redundant"])
    x_spam.append(quasar_size)
    y_spam.append(sample["quasar"]["update_spam"])


# setup plot
fig = plt.figure()
plot = fig.add_subplot(111)
plot.set_xlabel('Filter size')
plot.set_ylabel('Update calls')
# plot.set_xscale('log')
# plot.set_yscale('log')
plot.axis([0, 600, 0, 100])


# add plots
lines = plot.plot(x_success, y_success, 'k', label='Success %')
plt.setp(lines, color='green', linewidth=2.0)
lines = plot.plot(x_redundant, y_redundant, 'k', label='Redundant %')
plt.setp(lines, color='orange', linewidth=2.0)
lines = plot.plot(x_spam, y_spam, 'k', label='Spam %')
plt.setp(lines, color='red', linewidth=2.0)


# create legend
plot = plot.legend(loc='upper center', shadow=False, fontsize='small')
plot.get_frame().set_facecolor('#00FFFF')

# render
plt.savefig("benchmark/filterupdates_quasar_size_plot.png")
