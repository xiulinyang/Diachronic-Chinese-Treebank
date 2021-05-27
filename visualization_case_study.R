# data input
dat<- data.frame(Frequency,`1950-1965`,`1966-1976`,`1977-1999`,`2000-2010`)
data<-rbind(c(3.74,3.30,4.17,3.92), c(0.857, 0.861, 0.886, 0.850), c(30.58,	30.98,34.17,32.17))
rownames(data) = c('Modifier Frequency per Sentence','Subject frequency per sentence', 'Length of Sentence')
colnames(data)=c('1950-1965','1966-1976','1977-1999','2000-2010') 

data

# visualize three data
plot(data[1, ], type='o', pch= 2, ylim=range(1, data[1, ], data[3, ]), axes =FALSE, xlab = 'Periods', ylab='Frequency per sentence', main= 'Average frequency of modifier, subject and length of sentences')
axis(1, at =1:4, labels = colnames(data))
axis(2)
box()

lines(data[2, ], type = 'o', lty = 2, pch=0, col ='black')
lines(data[3, ], type='o', lty = 6, pch= 3, col='black')
legend('right', lty=c(1,2,6), col=c('black','black','black'), pch=c(2,0,3), legend =c('Modifier', 'Subject frequency per sentence', 'sentence length'), cex= 0.5)

plot(data[2, ], type='o', lty = 2, pch= 0, ylim=range(1, 0.7, data[2, ]), axes =FALSE, xlab = 'Periods', ylab='Frequency per sentence', main= 'Average frequency of subject of sentences')
axis(1, at =1:4, labels = colnames(data))
axis(2)
box()
legend('topright', lty=2, col='black', pch=0, legend =c('Subject frequency per sentence'), cex= 0.5)

plot(data[1, ], type='o', pch= 2, ylim=range(3, 2, 5), axes =FALSE, xlab = 'Periods', ylab='Frequency per sentence', main= 'Average frequency of modifier of sentences')
axis(1, at =1:4, labels = colnames(data))
axis(2)
box()
legend('bottomright', lty=2, col='black', pch=2, legend =c('Modifier frequency per sentence'), cex= 0.5)


