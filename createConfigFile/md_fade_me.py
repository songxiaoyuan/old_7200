# -*- coding:utf8 -*-
import csv
import basic_fun as bf
import os

TIME = 0
LASTPRICE = 1
MIDDLE = 2
SD = 3
RSI = 4
DIFF_VOLUME = 5
DIFF_OPENINTEREST = 6
SPREAD = 7
EMA_DIFF_VOLUME = 8
EMA_DIFF_OPENINTEREST = 9
EMA_SPREAD = 10
AVG_SUM = 12
LONG =1
SHORT =0

class BandAndTrigger(object):
	"""docstring for BandAndTrigger"""
	def __init__(self,param_dic):
		super(BandAndTrigger, self).__init__()
		# self.arg = arg
		self._direction = param_dic["direction"]

		self._moving_theo = "EMA"
		# now we have the cangwei and the limit cangwei
		self._now_interest = 0
		self._limit_interest = 1

		self._limit_max_draw_down = param_dic["limit_max_draw_down"]
		self._limit_max_loss = param_dic["limit_max_loss"]
		self._limit_max_profit = param_dic["limit_max_profit"]

		self._profit = 0
		self._max_profit = 0
		self._open_lastprice = 0

		self._bigger_Edge = param_dic["band_bigger"]
		self._limit_sd = param_dic["limit_sd"]


		self._band_status = 0

		# band param
		self._param_open_edge = param_dic["band_open_edge"]
		self._param_close_edge = param_dic["band_close_edge"]		

		# trigger param

		self._ris_data = 0

		self._file = param_dic["file"]


	def __del__(self):
		print "this is the over function"
		# bf.write_config_info(self._pre_ema_val,self._lastprice_array
		# 	,self._rsi_array,self._rsi_period,self._now_md_price[LASTPRICE],self._config_file)

	# get the md data ,every line;
	def get_md_data(self,md_array):
		# tranfer the string to float
		self._time = md_array[TIME]
		self._lastprice = float(md_array[LASTPRICE])
		self._now_middle_value = float(md_array[MIDDLE])
		self._now_sd_val = float(md_array[SD])

		if self._direction ==LONG:
			openval = self._now_middle_value - self._param_open_edge*self._now_sd_val
			if openval > self._lastprice :
				self._band_status = -1
		elif self._direction ==SHORT:
			openval = self._now_middle_value + self._param_open_edge*self._now_sd_val
			if self._lastprice > openval:
				self._band_status = 1

		open_time = self.is_trend_open_time()
		close_time = self.is_trend_close_time()
		# close_time = False
		
		if open_time and self._now_interest < self._limit_interest:
		# if open_time:
			self._open_lastprice = self._lastprice
			self._now_interest +=1
			self._max_profit = 0
			mesg= "the time of open: "+self._time + ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")
			# print "the diff volume is:" + str(self._now_md_price[VOLUME] - self._pre_md_price[VOLUME])
		# elif close_time:
		elif close_time and self._now_interest >0:
			# print "we need to close"
			if self._direction ==LONG:
				self._profit +=(self._lastprice - self._open_lastprice)
			elif self._direction ==SHORT:
				self._profit +=(self._open_lastprice - self._lastprice)
			self._open_lastprice = 0
			self._max_profit = 0
			self._now_interest = 0
			mesg= "the time of close:"+self._time+ ",the price: " + str(self._lastprice)
			self._file.write(mesg+"\n")

		return True

	def is_trend_open_time(self):

		is_band_open = self.is_band_open_time(self._direction,self._lastprice,
											self._now_middle_value,self._param_open_edge,self._now_sd_val,self._bigger_Edge)
		return is_band_open


	def is_trend_close_time(self):
		if self._now_interest <=0:
			return False
		# base the max draw down
		# 达到最大盈利之后，或者最大亏损之后，就开始平仓。这个是系统自带的。
		# 现在根据李总的说法，添加了maxdrawdown的功能。！！！！！
		if self._direction ==LONG:
			tmp_profit = self._lastprice - self._open_lastprice
		elif self._direction ==SHORT:
			tmp_profit = self._open_lastprice - self._lastprice
		else:
			return False
		if tmp_profit < (0 - self._limit_max_loss) or tmp_profit > self._limit_max_profit:
			# print "the profit is bigger or loss"
			return True

		is_drawdown = self.is_max_draw_down(self._direction,self._lastprice,self._open_lastprice
			,self._max_profit,self._limit_max_draw_down)
		self._max_profit = is_drawdown[1]
		if is_drawdown[0]:
			mesg= 'this is the max draw down ' + str(self._max_profit)
			self._file.write(mesg +"\n")
			return True

		is_band_close = self.is_band_close_time(self._direction,self._lastprice,
											self._now_middle_value,self._now_sd_val,
											self._param_open_edge,self._param_close_edge)
		
		return is_band_close


	def is_band_open_time(self,direction,lastprice,middle_val,open_edge,sd_val,bigger_edge):
		# this is used to judge is time to band open
		if sd_val <= self._limit_sd:
			return False
		if direction ==LONG:
			openval = middle_val - open_edge*sd_val
			if self._band_status == -1 and (self._lastprice - openval) > bigger_edge:
				self._band_status = 1
				return True
		elif direction ==SHORT:
			openval = middle_val + open_edge*sd_val
			if self._band_status == 1 and (openval - self._lastprice) > bigger_edge:
				self._band_status = -1
				return True
		return False

	def is_band_close_time(self,direction,lastprice,middle_val,sd_val,loss_edge,profit_edge):
		# this is used to judge is time to band open
		if direction ==LONG:
			profitval = middle_val + profit_edge*sd_val
			lossval = middle_val - loss_edge*sd_val 
			# if lastprice > profitval or lastprice < lossval:
			if lastprice > profitval:
				return True
		elif direction ==SHORT:
			profitval = middle_val - profit_edge*sd_val
			lossval = middle_val + loss_edge*sd_val
			# if lastprice > lossval or lastprice < profitval:
			if lastprice < profitval:
				return True
		return False


	def get_total_profit(self):
		return  self._profit

	def is_max_draw_down(self,direction,cur_price,open_price,max_profit,limit_max_draw_down):
		if open_price ==0 or limit_max_draw_down ==0:
			return (False,max_profit)
		if direction ==LONG:
			tmp_profit = cur_price - open_price;
		elif direction ==SHORT:
			tmp_profit = open_price - cur_price;
		else :
			return (False,0)
		tmp_profit = tmp_profit
		if max_profit < tmp_profit:
			max_profit = tmp_profit
		# f = open("rsidata.txt","a")
		# f.write(str(time)+","+str(cur_price)+","+str(open_price)+","+str(max_profit)+","+str(tmp_profit)+"\n")
		if (max_profit - tmp_profit) >= limit_max_draw_down :
			return (True,max_profit)
		else:
			return (False,max_profit)
		

def read_data_from_csv(path):
	f = open(path,'rb')
	reader = csv.reader(f)
	ret = []
	for row in reader:
		# obj.get_md_data(row)
		ret.append(row)
	# only get the day data
	return ret

def start_to_run_md(band_obj,data):
	for row in data:
		band_obj.get_md_data(row)

def create_band_obj(data,param_dict):
	file = param_dict["file"]
	for i in xrange(0,2):
		param_dict["direction"] = i
		if i==0:
			# continue
			# param_dict["limit_max_draw_down"] =0
			band_and_trigger_obj = BandAndTrigger(param_dict)
			print "方向是short的交易情况:"
			file.write("方向是short的交易情况:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")
		else:
			print "方向是long的交易情况："
			# param_dict["limit_max_draw_down"] =0
			band_and_trigger_obj = BandAndTrigger(param_dict)
			file.write("方向是long的交易情况：:\n")
			start_to_run_md(band_and_trigger_obj,data)
			profit = band_and_trigger_obj.get_total_profit()
			file.write(str(profit)+"\n")



def main(filename):
	path = "../everydayoutdata/"+filename+"_band_data.csv"
	# path = "../zn/"+filename
	csv_data = read_data_from_csv(path)
	path = "../fade_outdata/"+filename+"_trade_fade.txt"
	file = open(path,"w")

	# 这个是螺纹钢的 tick 1
	param_dict = {"limit_rsi_data":80,"band_open_edge":2,"band_close_edge":2,"limit_sd":0,
				"limit_max_profit":100000,"limit_max_loss":100,"limit_max_draw_down":1000,
				 "file":file,"band_bigger":4}
	if "rb" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =10
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =5
		param_dict["limit_sd"] =5
	elif "ru" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =50
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =25
		param_dict["limit_sd"] =25
	elif "pb" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =50
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =20
		param_dict["limit_sd"] =20
	elif "zn" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =50
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =20
		param_dict["limit_sd"] =20
	elif "cu" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =100
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =40
		param_dict["limit_sd"] =40
	elif "al" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =50
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =20
		param_dict["limit_sd"] =20
	elif "hc" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =10
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =4
		param_dict["limit_sd"] =4
	elif "i" in filename and "ni" not in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =5
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =2
		param_dict["limit_sd"] =2
	elif "ni" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =150
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =40
		param_dict["limit_sd"] =40
	elif "bu" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =20
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =8
		param_dict["limit_sd"] =8
	elif "pp" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =10
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =4
		param_dict["limit_sd"] =4
	elif "v" in filename:
		param_dict["limit_max_profit"] =50000
		param_dict["limit_max_loss"] =10
		param_dict["limit_max_draw_down"] =1000
		param_dict["band_bigger"] =4
		param_dict["limit_sd"] =4
	else:
		print "the instrument is not in the parm " + filename
		return
	create_band_obj(csv_data,param_dict)
	file.close()



if __name__=='__main__': 
	instrumentid = ["ru1801","rb1801","zn1711","pb1711","cu1711","hc1801","i1801","ni1801","al1711","pp1801","v1801","bu1712"]
	# instrumentid = ["ru1801","rb1801","zn1710","pb1710"]
	for instrument in instrumentid:
		path = instrument
		print path
		main(path)	
		# print WRITETOFILE