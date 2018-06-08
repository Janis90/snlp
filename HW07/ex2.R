##### Coffee vs. Not Coffee #####

# Black vs. not black
black <- c(500, 500)
n_black <- c(1000 + 100 + 400, 50 + 1200 + 9450)

chisq.test(data.frame(black,n_black))
# X-squared = 1019.1, df = 1, p-value < 2.2e-16


# Beans vs not beans
beans <- c(1000, 50)
n_beans <- c(500 + 100 + 400, 500 + 1200 + 9450)

chisq.test(data.frame(beans,n_beans))
# X-squared = 5684.5, df = 1, p-value < 2.2e-16


# Leaves vs. not leaves
leaves <- c(100, 1200)
n_leaves <- c(500 + 1000 + 400, 500 + 50 + 9450)

chisq.test(data.frame(leaves,n_leaves))
# X-squared = 61.768, df = 1, p-value = 3.864e-15


# Rest vs. not rest
rest <- c(400, 9450)
n_rest <- c(500 + 1000 + 100, 500 + 50 + 1200)

chisq.test(data.frame(rest,n_rest))
# X-squared = 3710, df = 1, p-value < 2.2e-16


##### Tea vs. Not Tea #####

# Black vs. not black
black <- c(750, 1000)
n_black <- c(110 + 1300 + 400, 1500 + 200 + 7350)

chisq.test(data.frame(black,n_black))
# X-squared = 637.33, df = 1, p-value < 2.2e-16


#Beans vs not beans
beans <- c(110, 1500)
n_beans <- c(750 + 1300 + 400, 1000 + 200 + 7350)

chisq.test(data.frame(beans,n_beans))
# X-squared = 205.99, df = 1, p-value < 2.2e-16


# Leaves vs. not leaves
leaves <- c(1300, 200)
n_leaves <- c(750 + 110 + 400, 1000 + 1500  + 7350)

chisq.test(data.frame(leaves,n_leaves))
# X-squared = 4629.8, df = 1, p-value < 2.2e-16


# Rest vs. not rest
rest <- c(400, 7350)
n_rest <- c(750 + 110 + 1300, 1000 + 1500  + 200)

chisq.test(data.frame(rest,n_rest))
# X-squared = 2846.4, df = 1, p-value < 2.2e-16