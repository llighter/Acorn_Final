

#install.packages('RMySQL')
library(RMySQL)


con <- dbConnect(dbDriver("MySQL"), host = "35.190.226.198", dbname = "test", user = "root", password = "abc123")
#dbListTables(con)  #DB abc에 있는 테이블목록 확인
dbSendQuery(con, 'set character set "utf8"')
test.table <- dbGetQuery(con, 'select * from testing')
#test.table['KRNAME']
df<- as.data.frame.matrix(test.table)


Encoding(df$KRNAME) <- "UTF-8"
Encoding(df$CONTRANT) <- "UTF-8"
Encoding(df$AGENCY) <- "UTF-8"
Encoding(df$GUARANTEE) <- "UTF-8"
Encoding(df$CHANGES) <- "UTF-8"
Encoding(df$CONDITIONS) <- "UTF-8"
Encoding(df$COMPONENT) <- "UTF-8"
Encoding(df$SOLD) <- "UTF-8"



#df
sapply(df,class)


form.full <- paste(names(df[! names(df) %in% c('PRICE', 'SRC', 'KRNAME')]),collapse ="+")
form.full <- paste("PRICE~", form.full) # same as full model PRICE~ all other variable with + sign between two variables.
modelp.full<-lm(as.formula(form.full), data = df)  # linear model of full model to test summary and anova.

#summary(modelp.full)
anova(modelp.full)

#install.packages('MASS')
library(MASS)
#stepAIC(modelp.full, direction="forward")
modelp.forward <- lm(formula = PRICE ~ ID + DATE + MODEL + GB + CONTRANT + AGENCY + 
                       GUARANTEE + CHANGES + CONDITIONS + COMPONENT + SOLD, data = df)

#stepAIC(modelp.full, direction="both")
#lm(formula = PRICE ~ MODEL + GB + CONDITIONS + COMPONENT, data = df)
modelp.both <- lm(formula = PRICE ~ MODEL + GB + CONDITIONS + COMPONENT, data = df)
adj <- summary(modelp.full)$adj.r.squared
anova(modelp.both)







