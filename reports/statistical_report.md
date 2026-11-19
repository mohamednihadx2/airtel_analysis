# **Airtel Telecom Analytics – Statistical Report**

Significance Level (α) = 0.05

## **1. Pre-offer Daily Data Usage – Group A vs Group B**

**Claim:** The two groups used the same amount of data before the offer.

**H₀:** Both groups have the same true average daily data before May.

**H₁:** The two averages differ.

**F-test:**

- F = 1.1108
- P = 3.673 × 10⁻⁸
- Decision: Variances differ.

**Z-test:**

- Z = 0.5191
- P = 0.6037

**Decision:** Fail to reject H₀.

**Conclusion:** There is insufficient evidence that the groups differed in their average daily data usage before the offer. The groups are considered balanced on this pre-offer measure.

## **2. Customer Characteristics – Group A vs Group B**

**Claim:** The customer characteristics of both groups have similar variance.

**H₀:** Both groups have equal variances.

**H₁:** The variances differ.

**F-test Results:**

| Variable        | F-value | P-value   |
| --------------- | ------- | --------- |
| Stated ARPU     | 1.0668  | 0.0006932 |
| Tenure Days     | 1.0244  | 0.2061    |
| Complaint Count | 1.0240  | 0.2128    |

**Decision:**

- Stated ARPU: Reject H₀.
- Tenure Days: Fail to reject H₀.
- Complaint Count: Fail to reject H₀.

**Conclusion:** Stated ARPU shows a significant variance difference between groups A and B. Tenure days and complaint count show no significant variance difference.

## **3. Pre-offer Revenue – Group A vs Group B**

**Claim:** Both groups paid the same amount on average before the offer.

**H₀:** Both groups have the same true average recharge revenue.

**H₁:** The two average revenues differ.

**F-test:**

- F = 0.9513
- P = 0.008866
- Decision: Variances differ.

**Z-test:**

- Z = -1.3490
- P = 0.1773

**Decision:** Fail to reject H₀.

**Conclusion:** There is insufficient evidence of a significant difference in average pre-offer revenue between the two groups.

## **4. Smartphone Users – Group A vs Group B**

**Claim:** Groups A and B have different proportions of smartphone users.

**H₀:** Both groups have the same true smartphone-user proportion.

**H₁:** The two proportions differ.

**Output:**

| Group | Total (n) | Smartphone (k) |
| ----- | --------- | -------------- |
| A     | 10996     | 9417           |
| B     | 11004     | 9554           |

**Z-test:**

- Z = 2.5457
- P = 0.01091

**Decision:** Reject H₀.

**Conclusion:** There is a statistically significant difference in smartphone-user proportions between groups A and B.

## **5. Prepaid Users – Group A vs Group B**

**Claim:** Groups A and B have different proportions of prepaid subscribers.

**H₀:** Both groups have the same true prepaid proportion.

**H₁:** The two proportions differ.

**Output:**

| Group | Total (n) | Prepaid (k) |
| ----- | --------- | ----------- |
| A     | 10996     | 8575        |
| B     | 11004     | 8574        |

**Z-test:**

- Z = -0.1177
- P = 0.9063

**Decision:** Fail to reject H₀.

**Conclusion:** There is no statistically significant difference in prepaid subscriber proportions between groups A and B.

## **6. Daily Data Usage After the Offer – Group A vs Group B**

**Claim:** The offer raised daily data usage.

**H₀:** Both groups have the same true average daily data in May and June.

**H₁:** Group B's average is higher.

**F-test:**

- F = 0.6197
- P = 8.402 × 10⁻¹¹⁶
- Decision: Variances differ.

**Z-test:**

- Z = -19.4496
- P = 2.936 × 10⁻⁸⁴

**Decision:** Reject H₀.

**Conclusion:** Group B has significantly higher average daily data usage after the offer. This supports the claim that the offer raised data usage.

## **7. Churn After the Offer – Group A vs Group B**

**Claim:** The offer reduced churn.

**H₀:** Both groups have the same true churn rate.

**H₁:** Group B's churn rate is lower.

**Z-test:**

- Z = 0.7937
- P = 0.4274

**Decision:** Fail to reject H₀.

**Conclusion:** There is insufficient evidence that the offer reduced churn. The observed churn rate in Group B is slightly higher than Group A.

## **8. Revenue After the Offer – Group A vs Group B**

**Claim:** The offer raised revenue.

**H₀:** Both groups paid the same on average.

**H₁:** Group B paid more.

**F-test:**

- F = 0.9697
- P = 0.1068
- Decision: No significant variance difference.

**Z-test:**

- Z = -0.5927
- P = 0.5534

**Additional T-test:**

- T = -0.5927
- P = 0.7233

**Decision:** Fail to reject H₀.

**Conclusion:** There is insufficient evidence that Group B paid more on average after the offer.

## **9. Prepaid vs Postpaid Churn**

**Claim:** Prepaid and postpaid subscribers churn at different rates.

**H₀:** Both have the same true churn rate.

**H₁:** The two rates differ.

**Output:**

| Group    | Total (n) | Churned (k) |
| -------- | --------- | ----------- |
| Postpaid | 4851      | 785         |
| Prepaid  | 17149     | 4441        |

**Z-test:**

- Z = 14.0364
- P = 9.333 × 10⁻⁴⁵

**Decision:** Reject H₀.

**Conclusion:** Prepaid and postpaid subscribers have significantly different churn rates. Prepaid subscribers have a higher churn rate.

## **10. Complaint Status vs Churn**

**Claim:** Subscribers with an open ticket churn at a different rate from those who never complained.

**H₀:** Both have the same true churn rate.

**H₁:** The two rates differ.

**Output:**

| Group      | Total (n) | Churned (k) |
| ---------- | --------- | ----------- |
| All Closed | 8689      | 2064        |
| Never      | 6631      | 1328        |
| Open       | 6680      | 1834        |

**Z-test:**

- Z = 10.0684
- P = 7.623 × 10⁻²⁴

**Decision:** Reject H₀.

**Conclusion:** Subscribers with open complaints have a significantly different churn rate from subscribers who never complained.

## **11. Year-0 vs Year-3 Subscriber Churn**

**Claim:** Year-0 and year-3 subscribers churn at different rates.

**H₀:** They share one true churn rate.

**H₁:** They do not.

**Output:**

| Group  | Total (n) | Churned (k) |
| ------ | --------- | ----------- |
| Year 0 | 4610      | 1328        |
| Year 3 | 3374      | 632         |

**Z-test:**

- Z = 10.3330
- P = 4.995 × 10⁻²⁵

**Decision:** Reject H₀.

**Conclusion:** Year-0 and year-3 subscribers have significantly different churn rates. Year-0 subscribers have a higher churn rate.

## **12. Himachal Pradesh vs Punjab Churn**

**Claim:** Himachal Pradesh and Punjab subscribers churn at different rates.

**H₀:** Both have the same true churn rate.

**H₁:** The two rates differ.

**Output:**

| Circle           | Total (n) | Churned (k) |
| ---------------- | --------- | ----------- |
| Himachal Pradesh | 1247      | 417         |
| Punjab           | 558       | 77          |

**Z-test:**

- Z = 0.6729
- P = 0.501

**Decision:** Fail to reject H₀.

**Conclusion:** There is insufficient evidence of a statistically significant difference in churn rates between Himachal Pradesh and Punjab.

## **13. Smartphone vs Feature Phone Churn**

**Claim:** Smartphone and feature-phone users churn at different rates.

**H₀:** Both have the same true churn rate.

**H₁:** The two rates differ.

**Output:**

| Device Type   | Total (n) | Churned (k) |
| ------------- | --------- | ----------- |
| Feature Phone | 3029      | 719         |
| Smartphone    | 18971     | 4507        |

**Z-test:**

- Z = 0.0241
- P = 0.9807

**Decision:** Fail to reject H₀.

**Conclusion:** There is no statistically significant difference in churn rates between smartphone and feature-phone users.

## **14. Gender vs Average Daily Data Usage**

**Claim:** Gender affects the average daily data usage of subscribers.

**H₀:** Both groups have the same true average daily data.

**H₁:** The two averages differ.

**F-test:**

- F = 0.9315
- P = 6.262 × 10⁻¹⁷⁷
- Decision: Variances differ.

**Z-test:**

- Z = -7.2519
- P = 4.109 × 10⁻¹³

**Decision:** Reject H₀.

**Conclusion:** Average daily data usage differs significantly between male and female subscribers. The female group has a lower sample average than the male group.

## **15. Feature Phone vs Smartphone Average Daily Data Usage**

**Claim:** Feature-phone and smartphone users have different average daily data usage.

**H₀:** Both groups have the same true average daily data usage.

**H₁:** The two averages differ.

**F-test:**

- F = 0.0268
- P = 0
- Decision: Variances differ.

**Z-test:**

- Z = -119.2400
- P = 0

**Decision:** Reject H₀.

**Conclusion:** Average daily data usage differs significantly between feature-phone and smartphone users. Smartphone users have a higher sample average.


