from pathlib import Path
import sys

algo_name=sys.argv[1]

Path('local/'+algo_name+'/input/data/training').mkdir(parents=True, exist_ok=True)
Path('local/'+algo_name+'/input/config').mkdir(parents=True, exist_ok=True)
Path('local/'+algo_name+'/model').mkdir(parents=True, exist_ok=True)

model_name=algo_name
print(algo_name)