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
    json.load(open("benchmark/filterupdates_quasar_refresh_a.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_b.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_c.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_d.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_e.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_f.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_g.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_h.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_i.json", "r")),
    json.load(open("benchmark/filterupdates_quasar_refresh_j.json", "r")),
]


for sample in samples:
    refresh_time = sample["quasar"]["constants"]["refresh_time"]
    x_success.append(refresh_time)
    y_success.append(sample["quasar"]["update_successful"])
    x_redundant.append(refresh_time)
    y_redundant.append(sample["quasar"]["update_redundant"])
    x_spam.append(refresh_time)
    y_spam.append(sample["quasar"]["update_spam"])


# setup plot
fig = plt.figure()
plot = fig.add_subplot(111)
plot.set_xlabel('Refresh time in sec.')
plot.set_ylabel('Update calls')
# plot.set_xscale('log')
# plot.set_yscale('log')
plot.axis([0, 100, 0, 100])


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
plt.savefig("benchmark/filterupdates_quasar_refresh_plot.png")
