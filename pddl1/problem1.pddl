(define (problem problem-14)
    (:domain regions)
    (:objects kasa_3 p_10_0 p_10_1 p_10_2 p_11_0 p_11_1 p_12_0 p_12_1 p_13_0 p_13_1 p_13_2 - location)
    (:init (connect-region kasa_3 kasa_3) (connect-region kasa_3 p_10_2) (connect-region kasa_3 p_11_1) (connect-region kasa_3 p_12_1) (connect-region kasa_3 p_13_2) (connect-region p_10_0 p_10_1) (connect-region p_10_0 p_11_0) (connect-region p_10_1 p_10_0) (connect-region p_10_1 p_10_2) (connect-region p_10_1 p_11_1) (connect-region p_10_2 kasa_3) (connect-region p_10_2 p_10_1) (connect-region p_11_0 p_10_0) (connect-region p_11_0 p_11_1) (connect-region p_11_0 p_12_0) (connect-region p_11_1 kasa_3) (connect-region p_11_1 p_10_1) (connect-region p_11_1 p_11_0) (connect-region p_11_1 p_12_1) (connect-region p_12_0 p_11_0) (connect-region p_12_0 p_12_1) (connect-region p_12_0 p_13_0) (connect-region p_12_1 kasa_3) (connect-region p_12_1 p_11_1) (connect-region p_12_1 p_12_0) (connect-region p_12_1 p_13_1) (connect-region p_13_0 p_12_0) (connect-region p_13_0 p_13_1) (connect-region p_13_1 p_12_1) (connect-region p_13_1 p_13_0) (connect-region p_13_1 p_13_2) (connect-region p_13_2 kasa_3) (connect-region p_13_2 p_13_1) (in-region p_10_2) (kasa kasa_3))
    (:goal (in-kasa))
)