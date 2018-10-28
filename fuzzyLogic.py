import csv, numpy as np, matplotlib.pyplot as plt

gaji = []
hutang = []


def trapesium(x, a, b, c, d):
    if (x <= a and x >= d):
        return 0
    elif (a < x < b):
        return (x - a) / float(b - a)
    elif (b <= x <= c):
        return 1
    elif (c < x < d):
        return -(x - d) / float(d - c)


def segitiga(x, a, b, c):
    if (x <= a and x >= c):
        return 0
    elif (a < x <= b):
        return (x - a) / float(b - a)
    elif (b < x <= c):
        return -(x - c) / float(c - b)


# Tahap Fuzzyfication

def keanggotaangaji(gajip):
    if (gajip >= 0 and gajip < 0.75):
        gaji.append(["Rendah", trapesium(gajip, 0, 0, 0.50, 0.75)])
    if (gajip > 0.5 and gajip < 1.50):
        gaji.append(["Normal", segitiga(gajip, 0.5, 1.25, 1.50)])
    if (gajip > 1.25 and gajip < 2):
        gaji.append(["Tinggi", trapesium(gajip, 1.25, 1.5, 2, 2)])


def keanggotaanhutang(hutangp):
    if (hutangp > 0 and hutangp < 40):
        hutang.append(["Rendah", trapesium(hutangp,0, 0, 20, 40)])
    if (hutangp > 20 and hutangp < 80):
        hutang.append(["Normal", segitiga(hutangp, 20, 60, 80)])
    if (hutangp > 60 and hutangp < 100):
        hutang.append(["Tinggi", trapesium(hutangp, 60, 80, 100, 100)])


# Tahap Inference

def fuzzyrules(gajip, hutangp):
    gajif = gajip[0]
    hutangf = hutangp[0]

    # Kondisi Rendah
    if (gajif == "Rendah" and hutangf == "Rendah"):
        return ["Tidak", min(gajip[1], hutangp[1])]
    if (gajif == "Rendah" and hutangf == "Normal"):
        return ["Iya", min(gajip[1], hutangp[1])]
    if (gajif == "Rendah" and hutangf == "Tinggi"):
        return ["Iya", min(gajip[1], hutangp[1])]

    # Kondisi Normal
    if (gajif == "Normal" and hutangf == "Rendah"):
        return ["Tidak", min(gajip[1], hutangp[1])]
    if (gajif == "Normal" and hutangf == "Normal"):
        return ["Tidak", min(gajip[1], hutangp[1])]
    if (gajif == "Normal" and hutangf == "Tinggi"):
        return ["Iya", min(gajip[1], hutangp[1])]

    # Kondisi Tinggi
    if (gajif == "Tinggi" and hutangf == "Rendah"):
        return ["Tidak", min(gajip[1], hutangp[1])]
    if (gajif == "Tinggi" and hutangf == "Normal"):
        return ["Tidak", min(gajip[1], hutangp[1])]
    if (gajif == "Tinggi" and hutangf == "Tinggi"):
        return ["Tidak", min(gajip[1], hutangp[1])]


def inference():
    hasil = [0, 0]
    for i in range(len(gaji)):
        for j in range(len(hutang)):
            p = fuzzyrules(gaji[i], hutang[j])
            if (p[0] == "Tidak" and hasil[0] < p[1]):
                hasil[0] = p[1]
            elif (p[0] == "Iya" and hasil[1] < p[1]):
                hasil[1] = p[1]
    return hasil


def defuzzy(inferencep):
    bobot = [40, 70]
    if((inferencep[0] != 0) and (inferencep[1]!=0)):
        return float(((inferencep[0] * bobot[0]) + (inferencep[1] * bobot[1])) / (inferencep[0] + inferencep[1]))
    elif(inferencep[0] != 0):
        return inferencep[0]*bobot[0]/inferencep[0]
    elif(inferencep[1] != 0):
        return inferencep[1]*bobot[1]/inferencep[1]
    else:
        return 0


file = open('./DataTugas2.csv', 'r')
mentahan = file.readlines()
indeks = 1
yangDapat = []
Gx,Gy = [],[]
for i in range(len(mentahan)):
    if(i!=0):
        data = mentahan[i].split(',')
        gajid = float(data[1])
        hutangd = float(data[2])
        keanggotaangaji(gajid)
        keanggotaanhutang(hutangd)
        inferensi = inference()
        defuzifikasi = defuzzy(inferensi)
        if (defuzifikasi > 50):
            yangDapat.append([i, gajid, hutangd, "Diterima",defuzifikasi])
        gaji = []
        hutang = []
def kunci(e):
    return e[4]
yangDapat.sort(key=kunci,reverse=True)
yangDapat2 = []
masukcsv = []
with open('./DataTugas2Tebakan.csv','w') as filecsv:
    filewriter = csv.writer(filecsv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Nomor','Pendapatan','Hutang','Status'])
    for i in range(20):
        yangDapat2.append(yangDapat[i])
        filewriter.writerow([str(yangDapat[i][0]),str(yangDapat[i][1]),str(yangDapat[i][2]),str(yangDapat[i][3])])
def kunci2(e):
    return e[0]
yangDapat2.sort(key=kunci2,reverse=False)
tx, ty, ti = [], [], []
for i in yangDapat2:
    ti.append(i[0])
    tx.append(i[1]) 
    ty.append(i[2])
plt.scatter(np.asarray(tx),np.asarray(ty))
for i in range(20):
    plt.annotate(ti[i],(tx[i],ty[i]))
plt.show()
