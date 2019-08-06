#chapter 5
# -*- coding: utf-8 -*-

import random
import math

menu_main=[] #メインメニューデータ(スマイル含む)
menu_side=[] #サイドメニューデータ
menu_drink=[] #ドリンクメニューデータ
menu_all=[] #全メニューデータ(メイン+サイド＋ドリンク)
kijunn = [] #食事摂取基準

#メインのメニュー読み込み
for line in file('mac_menu_main.csv'):
	menu_main.append(line.strip().split(','))

#サイドメニュー読み込み
for line in file('mac_menu_side.csv'):
	menu_side.append(line.strip().split(','))

#ドリンクメニュー読み込み
for line in file('mac_menu_drink.csv'):
	menu_drink.append(line.strip().split(','))

#全メニューデータ
menu_all= menu_main + menu_side + menu_drink

#食事摂取基準読み込み
for line in file('shokuji_sesshu_kijunn_data.csv'):
	kijunn = line.strip().split(',')

eng_kijunn=float(kijunn[0])/3 #energy
prt_kijunn=float(kijunn[1])/3 #protain
fat_kijunn=eng_kijunn*0.3/9.0 #fat
crb_kijunn=eng_kijunn*0.65/4 #carbon hydorates
kal_kijunn=float(kijunn[4])/3 #kalium
cal_kijunn=float(kijunn[5])/3 #calcium
rin_kijunn=float(kijunn[6])/3 #phosphorus=リン
irn_kijunn=float(kijunn[7])/3 #iron
va_kijunn=float(kijunn[8])/3 #vitamin A
vb1_kijunn=float(kijunn[9])/3 #vitamin B1
vb2_kijunn=float(kijunn[10])/3 #vitamin B2
ncn_kijunn=float(kijunn[11])/3 #niacin
vc_kijunn=float(kijunn[12])/3 #vitamin C
fbr_kijunn=float(kijunn[13])/3 #dietary fiber=食物繊維
slt_kijunn=float(kijunn[14])/3 #salt equivalent

#評価値を返す
#print_detail=Trueで詳細出力
#引数　メニューのidのリスト g=[1,2,3,4,5]とか
def evaluate(g=range(len(menu_main)), menu=menu_main, print_detail=False, all_nutrient=False):
	#たまにNoneが入るので無視　理由不明
	if g==None:
		print "None"
		return 0

	namelist=[]

	eng=0.0
	prt=0.0
	fat=0.0
	crb=0.0
	slt=0.0

	kal=0.0
	cal=0.0
	rin=0.0
	irn=0.0
	va=0.0
	vb1=0.0
	vb2=0.0
	ncn=0.0
	vc=0.0
	fbr=0.0

	fitness=0.0

	#個体gの栄養素を計算
	#指定したmenuから値を取ってきて足してく
	for i in range(len(g)):
		namelist.append(menu[g[i]][0])
		eng=eng+float(menu[g[i]][2]) #intだったけど大丈夫?
		prt=prt+float(menu[g[i]][3])
		fat=fat+float(menu[g[i]][4])
		crb=crb+float(menu[g[i]][5])
		slt=slt+float(menu[g[i]][18])

		if all_nutrient==True: #全栄養素調べるとき
			kal=kal+float(menu[g[i]][7])
			cal=cal+float(menu[g[i]][8])
			rin=rin+float(menu[g[i]][9])
			irn=irn+float(menu[g[i]][10])
			va=va+float(menu[g[i]][11])
			vb1=vb1+float(menu[g[i]][12])
			vb2=vb2+float(menu[g[i]][13])
			ncn=ncn+float(menu[g[i]][14])
			vc=vc+float(menu[g[i]][15])
			fbr=fbr+float(menu[g[i]][17])

	#栄養素ごとに評価
	eng_fit=gaussian(eng,eng_kijunn)
	prt_fit=gaussian(prt,prt_kijunn)
	fat_fit=gaussian(fat,fat_kijunn)
	crb_fit=gaussian(crb,crb_kijunn)
	slt_fit=gaussian(slt,slt_kijunn)

	if all_nutrient==True:
		#続く栄養素も評価
		kal_fit=gaussian(kal,kal_kijunn)
		cal_fit=gaussian(cal,cal_kijunn)
		rin_fit=gaussian(rin,rin_kijunn)
		irn_fit=gaussian(irn,irn_kijunn)
		va_fit=gaussian(va,va_kijunn)
		vb1_fit=gaussian(vb1,vb1_kijunn)
		vb2_fit=gaussian(vb2,vb2_kijunn)
		ncn_fit=gaussian(ncn,ncn_kijunn)
		vc_fit=gaussian(vc,vc_kijunn)
		fbr_fit=gaussian(fbr,fbr_kijunn)

	if all_nutrient==True:
		fitness=eng_fit+prt_fit+fat_fit+crb_fit+slt_fit+kal_fit+cal_fit+rin_fit+irn_fit+va_fit+vb1_fit+vb2_fit+ncn_fit+vc_fit+fbr_fit
		fitness=fitness/15.0
	else:
		fitness=eng_fit+prt_fit+fat_fit+crb_fit+slt_fit
		fitness=fitness/5.0

	#詳細を表示
	if print_detail==True:
		print namelist
		print "  energy total         : "+str(eng)+"/"+str(int(eng_kijunn)), str(int(eng/eng_kijunn*100))+"%", eng_fit
		print "  protain total        : "+str(prt)+"/"+str(int(prt_kijunn)), str(int(prt/prt_kijunn*100))+"%", prt_fit
		print "  fat total            : "+str(fat)+"/"+str(int(fat_kijunn)), str(int(fat/fat_kijunn*100))+"%", fat_fit
		print "  carbonhydorates total: "+str(crb)+"/"+str(int(crb_kijunn)), str(int(crb/crb_kijunn*100))+"%", crb_fit
		print "  salt equivalent total: "+str(slt)+"/"+str(int(slt_kijunn)), str(int(slt/slt_kijunn*100))+"%", slt_fit

		if all_nutrient==True:
			#残りの栄養素
			print "  kalium total         : "+str(kal)+"/"+str(int(kal_kijunn)), str(int(kal/kal_kijunn*100))+"%", kal_fit
			print "  calcium total        : "+str(cal)+"/"+str(int(cal_kijunn)), str(int(cal/cal_kijunn*100))+"%", cal_fit
			print "  rin total            : "+str(rin)+"/"+str(int(rin_kijunn)), str(int(rin/rin_kijunn*100))+"%", rin_fit
			print "  iron total           : "+str(irn)+"/"+str(int(irn_kijunn)), str(int(irn/irn_kijunn*100))+"%", irn_fit
			print "  vitaminA total       : "+str(va)+"/"+str(int(va_kijunn)), str(int(va/va_kijunn*100))+"%", va_fit
			print "  vitaminB1 total      : "+str(vb1)+"/"+str(vb1_kijunn), str(int(vb1/vb1_kijunn*100))+"%", vb1_fit
			print "  vitaminB2 total      : "+str(vb2)+"/"+str(vb2_kijunn), str(int(vb2/vb2_kijunn*100))+"%", vb2_fit
			print "  niacin total         : "+str(ncn)+"/"+str(int(ncn_kijunn)), str(int(ncn/ncn_kijunn*100))+"%", ncn_fit
			print "  vitaminC total       : "+str(vc)+"/"+str(int(vc_kijunn)), str(int(vc/vc_kijunn*100))+"%", vc_fit
			print "  dietary fiber total  : "+str(fbr)+"/"+str(int(fbr_kijunn)), str(int(fbr/fbr_kijunn*100))+"%", fbr_fit

		print "  fitness              :", fitness

	return fitness

#ガウス関数　分散は基準値+-20%
def gaussian(x, criteria=0, sigma=10.0):
	if  criteria != 0:
		sigma=0.4*criteria

	return math.e**(-(x-criteria)**2/(2*sigma**2))

def randomoptimize(fitnessf=evaluate):
	best=0.0
	bestr=None
	for i in range(1000):
		#generate solution randomly
		r=[random.randrange(0,len(menu_main)) for i in range(5)]

		#get fitness
		fitness=fitnessf(r)

		#compare with best solution
		if fitness>best:
			best=fitness
			bestr=r

	return r

def hillclimb(fitnessf=evaluate):
	#random solution
	sol=[random.randrange(0,len(menu_main)) for i in range(5)]

	#main loop
	while 1:
		neighbors=[]
		#neighbors: ランダムな解solのある要素を+-1した解すべてのリスト(solの近傍)
		for j in range(5):
			if sol[j]>0:
				neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
			if sol[j]<len(menu_main):
				neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
	
		#近傍中のベストを探索
		current=fitnessf(sol)
		best=current
		for j in range(len(neighbors)):
			fitness=fitnessf(neighbors[j])
			if fitness<best:
				best=fitness
				sol=neighbors[j]
	
		#改善がなければそれが最高
		if best==current:
			break
	
	return sol

def geneticoptimize(menu=menu_main, fitnessf=evaluate, popsize=50, len_gene=5, step=1, mutprob=0.2, elite=0.2, maxiter=100,all_nutrient=False):
	def mutate(vec):
		i=random.randint(0, len_gene-1)
		if random.random()<0.5 and vec[i]>0:
			return vec[0:i]+[vec[i]-step] + vec[i+1:]
		elif vec[i]<len(menu)-1:
			return vec[0:i]+[vec[i]+step]+vec[i+1:]

	def crossover(r1, r2):
		if len_gene==1 or len_gene==2 or len_gene==3:
			if random.random()>0.5:
				return r1
			else:
				return r2
		i=random.randint(1, len_gene-2) #遺伝子長の両端除いた数
		return r1[0:i]+r2[i:]

	#初期個体群構築
	pop=[]
	for i in range(popsize):
		vec=[random.randint(0, len(menu)-1) for i in range(len_gene)]
		pop.append(vec)

	topelite=int(elite*popsize)

	#main loop
	for i in range(maxiter):
		scores=[(fitnessf(g=v,menu=menu,all_nutrient=all_nutrient),v) for v in pop]
		scores.sort(reverse=True)
		ranked=[v for (s,v) in scores]

		#winner
		pop=ranked[0:topelite]

		#突然変異と交叉したものを追加
		while len(pop)<popsize:
			if random.random()<mutprob:
				#mutation
				c=random.randint(0,topelite)
				pop.append(mutate(ranked[c]))

			else:
				#crossover
				c1=random.randint(0,topelite)
				c2=random.randint(0,topelite)
				pop.append(crossover(ranked[c1], ranked[c2]))

		#present best
		print "gen%3d:" % int(i+1), scores[0][0]

	return scores[0][1]

    hoge = input()
