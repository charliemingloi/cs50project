import csv

score_id = {}
out = {}

with open('Yolov8\\test.csv', 'r') as file:
    csv_reader = csv.reader(file)
    
    next(csv_reader)
    
    for row in csv_reader:
        car_id1 = row[1].split(".")
        car_id = int(car_id1[0])
        score = float(row[6])
        number = row[5]
        
        if(car_id in score_id):
            if(score_id[car_id] < score):
                score_id[car_id] = score
                out[car_id] = number
        else:
            score_id[car_id] = score
            out[car_id] = number
        
print(out.values())