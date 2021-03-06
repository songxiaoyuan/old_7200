# -*- coding:utf8 -*-
import cx_Oracle  
import csv
import band_and_trigger
import basic_fun as bf
import shutil
import time
import os

LASTPRICE = 4
VOLUME = 11
OPENINTEREST = 13
TURNONER = 12
BIDPRICE1 = 22
ASKPRICE1 =24
TIME = 20
LONG =1
SHORT =0
date = time.strftime('%Y%m%d',time.localtime(time.time()))
hour = time.strftime('%H',time.localtime(time.time()))

# "info!!!! this must be run only once!!!!!!!!"
# 这个是铅的
param_dict_pb = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":50
			,"limit_rsi_data":75,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":20,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":310}

# 这个是螺纹钢的
param_dict_rb = {"limit_max_profit":25,"limit_max_loss":10,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":900,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":100,"open_interest_edge":0,"spread":100,"config_file":320}


# 这个是橡胶的
param_dic_ru = {"limit_max_profit":250,"limit_max_loss":100,"rsi_bar_period":100
			,"limit_rsi_data":70,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":120,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":330}

			
# 这个是锌的
param_dic_zn = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":340}


# 这个是锌的
param_dic_i = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":100,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":350}


# 这个是锌的
param_dic_ni = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":360}


param_dic_al = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":370}


# 这个是锌的
param_dic_hc = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":100
			,"limit_rsi_data":80,"rsi_period":10,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":380}


# 这个是锌的
param_dic_cu = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":1
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":70,"limit_max_draw_down":0,"multiple":10,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":390}



param_dic_pp = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":400}


param_dic_v = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":5,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":410}


param_dic_bu = {"limit_max_profit":125,"limit_max_loss":50,"rsi_bar_period":120
			,"limit_rsi_data":80,"rsi_period":14,"diff_period":60
			,"band_open_edge":0.5,"band_loss_edge":1,"band_profit_edge":3,"band_period":7200
			,"volume_open_edge":100,"limit_max_draw_down":0,"multiple":1,"file":file
			,"sd_lastprice":0,"open_interest_edge":0,"spread":100,"config_file":420}



nameDict = {
	"rb1805":{"param":[param_dict_rb]},
	"ru1801":{"param":[param_dic_ru]},
	"zn1712":{"param":[param_dic_zn]},
	"cu1711":{"param":[param_dic_cu]},
	"hc1801":{"param":[param_dic_hc]},
	"i1801":{"param":[param_dic_i]},
	"ni1801":{"param":[param_dic_ni]},
	"al1712":{"param":[param_dic_al]},
	"pp1801":{"param":[param_dic_pp]},
	"v1801":{"param":[param_dic_v]},
	"bu1712":{"param":[param_dic_bu]},
	"pb1712":{"param":[param_dict_pb]}
}

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()

		self._write_to_csv_data = []

		self._pre_md_price = []
		self._now_md_price = []
		self._lastprice_array = []
		self._lastprice_map = dict()
		self._pre_ema_val = 0
		self._now_middle_value =0
		self._now_sd_val = 0

		self._diff_volume_array = []
		self._diff_open_interest_array = []
		self._diff_spread_array = []
		self._diff_period =param_dic["diff_period"]

		self._multiple = param_dic["multiple"]

		self._rsi_array = []
		self._pre_rsi_lastprice =0 
		self._now_bar_rsi_tick = 0
		self._ris_data = 0
		self._rsi_period = param_dic["rsi_period"]
		self._rsi_bar_period = param_dic["rsi_bar_period"]
		self._limit_rsi_data = param_dic["limit_rsi_data"]

		# self._limit_twice_sd = 2

		self._moving_theo = "EMA"
		# band param
		self._param_period = param_dic["band_period"]


		self._file = param_dic["file"]
		self._config_file = param_dic["config_file"]

		if len(self._lastprice_array) ==0:
			print "this is init function"
			tmp_pre_ema_array = []
			tmp_rsi_lastprice = []
			config_file = "../config_server/"+str(self._config_file)
			bf.get_config_info(tmp_pre_ema_array,self._lastprice_array,self._lastprice_map
				,self._rsi_array,tmp_rsi_lastprice,config_file)
			if len(tmp_pre_ema_array)==0:
				self._pre_ema_val = 0
				self._pre_rsi_lastprice = 0 
			else:
				self._pre_ema_val = tmp_pre_ema_array[0]
				self._pre_rsi_lastprice = tmp_rsi_lastprice[0]
		print self._pre_ema_val
		print len(self._lastprice_array)
		print self._rsi_array
		print self._pre_rsi_lastprice
		# print "the length of lastprice is: " +str(len(self._lastprice_array))


	def __del__(self):
		print "this is the over function"
		config_file = "../config_server/"+str(self._config_file)
		bf.write_config_info(self._pre_ema_val,self._lastprice_array
			,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],config_file)

		config_file = "../config_server/"+str(self._config_file+1)
		bf.write_config_info(self._pre_ema_val,self._lastprice_array
			,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],config_file)

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		# md_array[LASTPRICE] = float(md_array[LASTPRICE])
		# md_array[VOLUME] = float(md_array[VOLUME])
		# md_array[OPENINTEREST] = float(md_array[OPENINTEREST])
		# md_array[TURNONER] = float(md_array[TURNONER])
		# md_array[BIDPRICE1] = float(md_array[BIDPRICE1])
		# md_array[ASKPRICE1] = float(md_array[ASKPRICE1])


		self._pre_md_price = self._now_md_price
		self._now_md_price = md_array

		lastprice = self._now_md_price[LASTPRICE]
		if len(self._pre_md_price) ==0:
			return
		else:
			# self._rsi_array.append(lastprice - self._pre_md_price[LASTPRICE])
			if self._now_bar_rsi_tick >= self._rsi_bar_period:
				# 表示已经到了一个bar的周期。
				tmpdiff = lastprice - self._pre_rsi_lastprice		
				self._pre_rsi_lastprice = lastprice
				self._now_bar_rsi_tick = 1
				self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				self._rsi_array.append(tmpdiff)
			else:
				self._now_bar_rsi_tick +=1
				tmpdiff = lastprice - self._pre_rsi_lastprice
				self._ris_data =bf.get_rsi_data2(tmpdiff,self._rsi_array,self._rsi_period)
				# self._ris_data = 0

		# if len(self._lastprice_array) > self._param_period:
		# 	self._lastprice_array.pop(0)

		self._lastprice_array.append(lastprice)

		if len(self._lastprice_array) <= self._param_period:
			# this is we dont start the period.
			# print  "the lastprice length is small: " +str(len(self._lastprice_array))
			ema_period = len(self._lastprice_array)
			pre_ema_val = bf.get_ema_data(lastprice,self._pre_ema_val,ema_period)
			self._pre_ema_val = pre_ema_val
			# save the pre_ema_val and return
			if lastprice not in self._lastprice_map:
				self._lastprice_map[lastprice] =1
			else:
				self._lastprice_map[lastprice] +=1
			return True

		front_lastprice = self._lastprice_array[0]
		self._lastprice_array.pop(0)
		if front_lastprice != lastprice:
			if lastprice not in self._lastprice_map :
				self._lastprice_map[lastprice] = 1
			else:
				self._lastprice_map[lastprice] +=1

			self._lastprice_map[front_lastprice] -=1
		# start the judge
		if self._moving_theo =="EMA":
			self._now_middle_value = bf.get_ema_data(lastprice,self._pre_ema_val,self._param_period)
			self._pre_ema_val = self._now_middle_value
		else:
			self._now_middle_value = bf.get_ma_data(self._lastprice_array,self._param_period)
		
		self._now_sd_val =bf.get_sd_data_by_map(self._lastprice_map,self._param_period)	
	
		return True


def start_create_config(instrumentid,data):
	print "start create the config file of " + instrumentid
	if instrumentid not in nameDict:
		print "the instrument id " + instrumentid + " is not in the dict"
	for param in nameDict[instrumentid]["param"]:
		bt = BandAndTrigger(param)
		for row in data:
			bt.get_md_data(row)
			# tranfer the string to float


def getSortedData(data):
	ret = []
	night = []
	zero = []
	day = []
	nightBegin = 21*3600
	nightEnd = 23*3600+59*60+60
	zeroBegin = 0
	zeroEnd = 9*3600 - 100
	dayBegin = 9*3600
	dayEnd = 15*3600

	for line in data:
		# print line
		timeLine = line[20].split(":")
		# print timeLine
		try:
			nowTime = int(timeLine[0])*3600+int(timeLine[1])*60+int(timeLine[2])
		except Exception as e:
			nowTime = 0

		if nowTime >= zeroBegin and nowTime <zeroEnd:
			zero.append(line)
		elif nowTime >= dayBegin and nowTime <= dayEnd:
			day.append(line)
		elif nowTime >=nightBegin and nowTime <=nightEnd:
			night.append(line)
		# if int(line[22]) ==0 or int(line[4]) ==3629:
		# 	continue
	night = sorted(night, key = lambda x: (x[20], int(x[21])))
	zero = sorted(zero, key = lambda x: (x[20], int(x[21])))
	day = sorted(day, key = lambda x: (x[20], int(x[21])))
	if int(hour) >= 15:
		print "this is afternoon dont need the night data"
	else:	
		for line in night:
			ret.append(line)
		for line in zero:
			ret.append(line)
	for line in day:
		ret.append(line)

	return ret

def copy_file():
	print "start create the real server data"
	shutil.copy('../config_server/340', '../real_server/520')
	shutil.copy('../config_server/340', '../real_server/521')
	shutil.copy('../config_server/320', '../real_server/522')
	shutil.copy('../config_server/320', '../real_server/523')
	shutil.copy('../config_server/330', '../real_server/524')
	shutil.copy('../config_server/330', '../real_server/525')
	shutil.copy('../config_server/310', '../real_server/526')
	shutil.copy('../config_server/310', '../real_server/527')

	# shutil.copy('../config_server/310', '../config_server/312')
	# shutil.copy('../config_server/310', '../config_server/313')
	# shutil.copy('../config_server/310', '../config_server/314')
	# shutil.copy('../config_server/310', '../config_server/315')
	# shutil.copy('../config_server/320', '../config_server/322')
	# shutil.copy('../config_server/320', '../config_server/323')
	# shutil.copy('../config_server/320', '../config_server/324')
	# shutil.copy('../config_server/320', '../config_server/325')
	# shutil.copy('../config_server/330', '../config_server/332')
	# shutil.copy('../config_server/330', '../config_server/333')
	# shutil.copy('../config_server/330', '../config_server/334')
	# shutil.copy('../config_server/330', '../config_server/335')
	# shutil.copy('../config_server/340', '../config_server/342')
	# shutil.copy('../config_server/340', '../config_server/343')
	# shutil.copy('../config_server/340', '../config_server/344')
	# shutil.copy('../config_server/340', '../config_server/345')
	# shutil.copy('../config_server/350', '../config_server/352')
	# shutil.copy('../config_server/350', '../config_server/353')
	# shutil.copy('../config_server/350', '../config_server/354')
	# shutil.copy('../config_server/350', '../config_server/355')
	# shutil.copy('../config_server/360', '../config_server/362')
	# shutil.copy('../config_server/360', '../config_server/363')
	# shutil.copy('../config_server/360', '../config_server/364')
	# shutil.copy('../config_server/360', '../config_server/365')
	# shutil.copy('../config_server/370', '../config_server/372')
	# shutil.copy('../config_server/370', '../config_server/373')
	# shutil.copy('../config_server/370', '../config_server/374')
	# shutil.copy('../config_server/370', '../config_server/375')
	# shutil.copy('../config_server/380', '../config_server/382')
	# shutil.copy('../config_server/380', '../config_server/383')
	# shutil.copy('../config_server/380', '../config_server/384')
	# shutil.copy('../config_server/380', '../config_server/385')
	# shutil.copy('../config_server/390', '../config_server/392')
	# shutil.copy('../config_server/390', '../config_server/393')
	# shutil.copy('../config_server/390', '../config_server/394')
	# shutil.copy('../config_server/390', '../config_server/395')
	# shutil.copy('../config_server/400', '../config_server/404')
	# shutil.copy('../config_server/400', '../config_server/405')
	# shutil.copy('../config_server/410', '../config_server/414')
	# shutil.copy('../config_server/410', '../config_server/415')
	# shutil.copy('../config_server/420', '../config_server/424')
	# shutil.copy('../config_server/420', '../config_server/425')

def copy_file_one_to_one(from_path,to_path):
	for root, dirs, files in os.walk(from_path):
	    for file in files:
    		tmp_path = os.path.join(root,file)
    		# print tmp_path
    		shutil.copy(tmp_path, to_path+file)

def copy_file_to_pic():
	path = "../pic-server/HelloWorld/config_server/"
	for root, dirs, files in os.walk(path):
	    for file in files:
    		tmp_path = os.path.join(root,file)
    		# print tmp_path
    		os.remove(tmp_path)
	from_path = "../config_server/"
	copy_file_one_to_one(from_path,path)
	

def copy_file_to_save():
	path = "../save_config_file/"
	new_path = os.path.join(path, date)
	if not os.path.isdir(new_path) and os.path.isdir(path):
	    os.mkdir(new_path)
	copy_file_one_to_one("../config_server/",new_path+'/')

def getSqlData(myday,instrumentid): 

	conn = cx_Oracle.connect('hq','hq','114.251.16.210:9921/quota')    
	cursor = conn.cursor () 

	mysql="select *from hyqh.quotatick where TRADINGDAY = '%s' AND INSTRUMENTID = '%s'" % (str(myday),instrumentid)

	print mysql
	cursor.execute (mysql)  
	icresult = cursor.fetchall()

	cleandata = getSortedData(icresult)
	start_create_config(instrumentid,cleandata)



if __name__=='__main__':
	instrumentid_array = ["ru1801","rb1805","zn1712","pb1712"]
	for instrumentid in instrumentid_array:
		getSqlData(date,instrumentid)	

	copy_file()
	if int(hour)<9:
		copy_file_to_pic()
		copy_file_to_save()