TEST = data/plan_base.xlsx 

main: main.py
	python3.8 $< ${TEST}
