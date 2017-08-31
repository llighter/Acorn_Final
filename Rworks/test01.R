

#install.packages('RMySQL')
library(RMySQL)
library(MASS) # forward , both 
library(car) #outlierTest, influencePlot
library(ggplot2) # qplot

con <- dbConnect(dbDriver("MySQL"), host = "35.190.226.198", dbname = "apple", user = "root", password = "abc123")
#dbListTables(con)  #DB abc에 있는 테이블목록 확인
dbSendQuery(con, 'set character set "utf8"')
test.table <- dbGetQuery(con, '
                         SELECT
                          A.*
                         FROM
                         (
                         SELECT
                         @ROWNUM := @ROWNUM + 1 AS ROWNUM,
                         total_iphone.* 
                         FROM
                         total_iphone,
                         (SELECT @ROWNUM := 0) R
                         ) A
                         WHERE
                         A.ROWNUM < 60000
                         ')
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
Encoding(df$CONTRACT) <- "UTF-8"

df$PRICE <- as.numeric(df$PRICE)
df$MODEL<- df$MODEL


# df
#sapply(df,class)


form.full <- paste(names(df[! names(df) %in% c('PRICE', 'SRC', 'KRNAME', 'CONTRANT', 'GUARANTEE', 'CHANGES', 'CONDITIONS', 'COMPONENT')]),collapse ="+")
form.full <- paste("PRICE~", form.full) # same as full model PRICE~ all other variable with + sign between two variables.
modelp.full<-lm(as.formula(form.full), data = df)  # linear model of full model to test summary and anova.

#summary(modelp.full)
anova(modelp.full)

#install.packages('MASS')
#stepAIC(modelp.full, direction="forward")
modelp.forward <- lm(formula = PRICE ~ ID + DATE + MODEL + GB + CONTRANT + AGENCY + 
                       GUARANTEE + CHANGES + CONDITIONS + COMPONENT + SOLD, data = df)

#stepAIC(modelp.full, direction="both")
#lm(formula = PRICE ~ MODEL + GB + CONDITIONS + COMPONENT, data = df)
modelp.both <- lm(formula = PRICE ~ MODEL + GB + CONDITIONS + COMPONENT, data = df)

modelp.none <-PRICE ~ MODEL + GB + CONDITIONS + COMPONENT

adj <- summary(modelp.full)$adj.r.squared
anova(modelp.both)


summary(modelp.both)
summary(modelp.both)$coefficients['MODELA1332']
coef(summary(modelp.both))
ls(summary(modelp.both))



coefficients(summary(modelp.both))
terms(summary(modelp.both))


outlierTest(modelp.both) # output: observation outlier!
influencePlot(modelp.both)

ls(outlierTest(modelp.both))
outlierTest(modelp.both)

boxplot( PRICE~ KRNAME, groups = MODEL, data=df)
  #xyplot(PRICE~ RELDATE, data = df, rm.na = T)

qplot(PRICE, KRNAME, data = df, color = MODEL, size = KRNAME)











