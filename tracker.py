from calendar import timegm
from datetime import datetime
from matplotlib import colormaps
from time import time
import numpy as np

class Tracker:
	def __init__(self) -> None:
		self.xx_mesh, self.yy_mesh = np.mgrid[1:32, 1:13]
		self.all_cnts = np.zeros((31, 12))

	def convertRawData(self, input_file: str, output_file: str, yy_0: int, mm_0: int, dd_0: int):
		self.rawGetCounts(input_file, yy_0, mm_0, dd_0)
		return self.saveCounts(output_file)

	def customColours(self) -> list[str]:
		def hexify(c: int) -> str:
			d = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}
			return d[c // 16] + d[c % 16]

		max_faps = int(self.all_cnts.max())

		cmap = colormaps.get("Blues", 256)
		custom_clrs = ["#C0C0C0", "#808080", "#FFFFFF"]

		for clr in [cmap(int((i + 1) * 255 / max_faps)) for i in range(max_faps)]:
			custom_clrs.append(f"#{hexify(int(clr[0] * 255))}{hexify(int(clr[1] * 255))}{hexify(int(clr[2] * 255))}")

		return custom_clrs

	def getCounts(self, from_file: str, update: bool = True) -> tuple:
		if update:
			self.all_cnts = np.fromfile(from_file).reshape((31, 12))
			return self.xx_mesh, self.yy_mesh, self.all_cnts
		temp_all_cnts = np.fromfile(from_file).reshape((31, 12))
		return self.xx_mesh, self.yy_mesh, temp_all_cnts

	def rawGetCounts(self, input_file: str, yy_0: int, mm_0: int, dd_0: int) -> tuple:
		with open(input_file, 'r') as fp:
			raw_lines = fp.readlines()

		# yy_0, mm_0, dd_0 = 2024, 7, 23
		ref_uts = timegm(datetime(yy_0, mm_0, dd_0, 0, 0, 0).timetuple())
		curr_uts = int(time())
		mm_curr, dd_curr = map(int, datetime.fromtimestamp(curr_uts).strftime("%m %d").split(' '))

		SECS_PER_DAY = 86400
		n_days = int((curr_uts - ref_uts) // SECS_PER_DAY + 2)
		print(ref_uts, curr_uts, n_days)
		cnts = [0] * n_days
		# dates = [tuple(map(int, datetime.fromtimestamp(ref_uts + i * SECS_PER_DAY).strftime("%m %d").split(' '))) for i in range(n_days)]

		# all_dates = np.mgrid[1:32, 1:13].reshape(2, -1).T
		self.all_cnts[:, :mm_0 - 1] = -2
		self.all_cnts[:dd_0 - 1, mm_0 - 1] = -2
		self.all_cnts[dd_curr:, mm_curr - 1] = -2
		self.all_cnts[:, mm_curr:] = -2
		self.all_cnts[29, 1] = self.all_cnts[30, 1] = self.all_cnts[30, 3] = self.all_cnts[30, 5] = self.all_cnts[30, 8] = self.all_cnts[30, 10] = -1

		for line in raw_lines:
			msg = line[30:].strip()
			if msg[0] == 'i':
				dd, mm, yy = map(int, line[1:9].split('/'))
				yy += 2000
				uts = timegm(datetime(yy, mm, dd).timetuple())
				if uts >= ref_uts:
					if len(msg) > 1:
						dd, mm, yy = map(int, msg[3:-1].split('/'))
						uts = timegm(datetime(yy, mm, dd).timetuple())
					cnts[int((uts - ref_uts) // SECS_PER_DAY)] += 1
					self.all_cnts[dd - 1, mm - 1] += 1

		return self.xx_mesh, self.yy_mesh, self.all_cnts

	def saveCounts(self, output_file: str):
		self.all_cnts.tofile(output_file)
		return True

	def updateCounts(self, diff: int) -> tuple:
		curr_uts = int(time())
		mm_curr, dd_curr = map(int, datetime.fromtimestamp(curr_uts).strftime("%m %d").split(' '))
		self.all_cnts[dd_curr - 1, mm_curr - 1] = max(self.all_cnts[dd_curr - 1, mm_curr - 1] + diff, 0.0)
		return self.xx_mesh, self.yy_mesh, self.all_cnts
