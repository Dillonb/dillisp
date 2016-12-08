(defn facit (acc n)
    (if (< n 2)
        acc
        (facit (* acc n) (- n 1))))

(defn fac (n)
    (facit 1 n))

(print (fac 1))
(print (fac 2))
(print (fac 3))
(print (fac 4))
(print (fac 5))
(print (fac 6))
(print (fac 7))
(print (fac 8))
(print (fac 9))
(print (fac 10))

(print (fac 20000))
