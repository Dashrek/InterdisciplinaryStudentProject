(define (domain regions)
    (:requirements :adl :strips :typing)
    (:types item location)
    (:predicates (connect-region ?x - location ?z - location)  (from-region ?x - location ?y - item)  (in-backpack ?y - item)  (in-kasa) (in-region ?x - location)  (kasa ?x - location))
    (:action move-to-region
        :parameters (?x - location ?z - location)
        :precondition (and (in-region ?x) (connect-region ?x ?z))
        :effect (and (not (in-region ?x)) (in-region ?z))
    )
     (:action take-to-backpack
        :parameters (?x - location ?y - item)
        :precondition (and (in-region ?x) (from-region ?x ?y))
        :effect (in-backpack ?y)
    )
     (:action zaplac
        :parameters (?x - location)
        :precondition (and (in-region ?x) (kasa ?x))
        :effect (and (not (in-region ?x)) (in-kasa))
    )
)