(define (problem problem-1)
    (:domain regions)
    (:objects kasa_2 p_7_0 p_7_1 p_7_2 p_8_0 p_8_1 p_9_0 p_9_1 - location)
    (:init (connect-region kasa_2 kasa_2) (connect-region kasa_2 p_7_2) (connect-region kasa_2 p_8_1) (connect-region kasa_2 p_9_1) (connect-region p_7_0 p_7_1) (connect-region p_7_0 p_8_0) (connect-region p_7_1 p_7_0) (connect-region p_7_1 p_7_2) (connect-region p_7_1 p_8_1) (connect-region p_7_2 kasa_2) (connect-region p_7_2 p_7_1) (connect-region p_8_0 p_7_0) (connect-region p_8_0 p_8_1) (connect-region p_8_0 p_9_0) (connect-region p_8_1 kasa_2) (connect-region p_8_1 p_7_1) (connect-region p_8_1 p_8_0) (connect-region p_8_1 p_9_1) (connect-region p_9_0 p_8_0) (connect-region p_9_0 p_9_1) (connect-region p_9_1 kasa_2) (connect-region p_9_1 p_8_1) (connect-region p_9_1 p_9_0) (in-region kasa_2) (kasa kasa_2))
    (:goal (in-kasa))
)