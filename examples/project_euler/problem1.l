(defn three-or-five? (n) (or (= 0 (% n 3)) (= 0 (% n 5))))
(print (reduce (lambda (x y) (+ x y)) (filter three-or-five? (range 1 1000))))
