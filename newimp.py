
def airport_schedule(n, r, c, matrix, event_list):
    parking_spaces = {}
    for i in range(r):
        for j in range(c):
            square = row[j]
            if square == '==':
                matrix[i][j] = 'land'
            elif square == '..':
                matrix[i][j] = 'empty'
            elif square == '##':
                matrix[i][j] = 'obstacle'
            else:
                matrix[i][j] = 'parking'
                parking_spaces[square] = False
    
    #Create a dictionary to keep track of which parking spaces are occupied
    def find_empty_parking_space():
        for ps, occupied in parking_spaces.items():
            if not occupied:
                return ps
        return None
    
    #For each event in the event list, find a feasible landing or takeoff location,
    #assign a parking space to the airplane, and mark the parking space as occupied in the dictionary
    assigned_parking_spaces = [None] * n
    for event in event_list:
        if event > 0:  # Landing event
            plane = event
            for i in range(r):
                for j in range(c):
                    if matrix[i][j] == 'land':
                        #Check if the path to the parking space is clear
                        clear_path = True
                        for k in range(i+1, r):
                            if matrix[k][j] == 'obstacle':
                                clear_path = False
                                break
                            if matrix[k][j] == 'parking' and parking_spaces[matrix[k][j+1]]:  # Parking space is occupied
                                clear_path = False
                                break
                        if clear_path:
                            #Assign a parking space to the airplane
                            parking_space = find_empty_parking_space()
                            if parking_space is None:
                                return "No"
                            assigned_parking_spaces[plane-1] = parking_space
                            parking_spaces[parking_space] = True
                            #Mark the parking space as occupied in the flat land layout
                            for k in range(i+1, r):
                                if matrix[k][j] == 'parking':
                                    matrix[k][j+1] = parking_space
                                else:
                                    break
                            break
            else:
                return "No"
        else:  #takeoff event
            plane = -event
            parking_space = assigned_parking_spaces[plane-1]
            for i in range(r):
                for j in range(c):
                    if matrix[i][j] == 'parking' and matrix[i][j+1] == parking_space:
                        #Check if the path to the takeoff location is clear
                        clear_path = True
                        for k in range(j+1, c):
                            if matrix[i][k] == 'obstacle':
                                clear_path = False
                                break
                            if matrix[i][k] == 'land' or matrix[i][k] == 'parking':
                                clear_path = False
                                break
                    if clear_path:
                        # Mark the parking space as unoccupied in the dictionary
                        parking_spaces[parking_space] = False
                        # Mark the parking space as unoccupied in the flat land layout
                        for k in range(i, r):
                            if matrix[k][j] == 'parking' and matrix[k][j+1] == parking_space:
                                matrix[k][j+1] = None
                            else:
                                break
                        assigned_parking_spaces[plane-1] = None
                        break
                else:
                    return "No"
# Output the assigned parking spaces
    return "Yes\n" + ' '.join([f"{ps:02d}" for ps in assigned_parking_spaces])

#input
case_num = 1
while True:
    n, r, c = map(int, input("ingrese datos:").split())
    if n == 0:
        break
    land = []
    for i in range(r):
        print("row",i)
        row = input().split()
        land.append(row)
        
    events = map(int, input("events").split())
    result = airport_schedule(n, r, c, land, events)
    print("3")
    print(f"Case {case_num}: {result}")
    case_num += 1
