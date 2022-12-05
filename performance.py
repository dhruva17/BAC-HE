import matplotlib.pyplot as plt
  
x = []
y = []
for line in open('time.txt', 'r'):
    lines = [i for i in line.split()]
    x.append(lines[0])
    y.append(int(lines[1]))
      
plt.title("Time taken vs size of database")
plt.xlabel('Time')
plt.ylabel('Size of database')
plt.yticks(y)
plt.plot(x, y, marker = 'o', c = 'g')
  
plt.show()
