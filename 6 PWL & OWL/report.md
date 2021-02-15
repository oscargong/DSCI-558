# HW6 PSL & OWL

## Task 1 PSL

### Task 1.1

![screenshot ](https://i.loli.net/2020/10/22/yJlpqE6G2IVm3Kj.png)

A live and full version of screenshot is available here: https://asciinema.org/a/0UzGSWWM0fAEIwAtrFDqKBjt7

###  Task 1.2

### 1.2.1 Similarity

- I use Jaro–Winkler as the similiaty metric for title. I first lowercase it, remove the punctuation, and then calculate the similarities
- I use the normalized Levenshtein as the similiaty metric for year. If one year filed is empty, then it will be scored `0.5`.

### 1.2.2 `model-manual.psl`

A snapshot of terminal output:

```pseudocode
[main] INFO  org.linqs.psl.cli.Launcher  - Evaluation results for SAMEPAPER -- Accuracy: 0.997671, F1: 0.794979, Positive Class Precision: 0.860507, Positive Class Recall: 0.738725, Negative Class Precision: 0.998394, Negative Class Recall: 0.999263
```

### 1.2.3 `model-learned.psl`

A snapshot of terminal output:

```pseudocode
[main] INFO  org.linqs.psl.cli.Launcher  - Evaluation results for SAMEPAPER -- Accuracy: 0.997281, F1: 0.719608, Positive Class Precision: 0.973475, Positive Class Recall: 0.570762, Negative Class Precision: 0.997366, Negative Class Recall: 0.999904
```

---



## Task 2 OWL

### Task 2.1 Pizza Ontology

The tutorial is quite outdated, the interface and lots of functions look different from the current version. Several times, I had trouble figuring out what it was referring to.

#### Problems encountered on Task 2.1

**0:**

![trouble 0.png](https://i.loli.net/2020/10/26/R2GAKbWT6chtXSk.png)

1: No matching option exist, I choose the closest one: `End with` -> `Auto-generated ID`

2: No matching option exist, I choose the closest one: `Render by annotation property (e.g., rdfs:label, skos:prefLabel)`

**1：**
![trouble 1.png](https://i.loli.net/2020/10/26/U8Ex6AIjanM97wV.png)


- 1 and 2 in different spell
- 3: `Qutr...pizza` cannot be found on previous image, thus I skipped this one 

**2. **
![trouble 2.png](https://i.loli.net/2020/10/26/5HQr9MIJVXbvUje.png)

Cannot found `Fish_topping` , never mentioned on previous part of tutorial, thus I skipped. Accordingly , `Vegetarian_pizza`  's definition becomes `Pizza and not(has_topping some Meat_topping)`

**3. **
![trouble 3.png](https://i.loli.net/2020/10/26/4ULi7VgabDFE8ve.png)

- 1: No matching menu item exist, I choose the closest one: `remove local disjoint classes axioms...`
- 2: Shorcut not working at all

**4. Other Bugs I met**

       1. Using a reasoner may cause the hierarchy of class to be out of order.
       2. Save the owl file and re-read it, the hierarchy of class may be incorrect.

### Task 2.2 Protégé - `people.owl`

#### 2.2.1 Mad Cow

> 2.2.1.1. What’s the definition of mad_cow?
> Give both the formal definition and an explanation in your own words.

- Formal: 

    - A mad cow is a cow that has been eating the brains of sheep.

    - ```pseudocode
        cow and (eats some (brain and (part_of some sheep)))
        ```

- My explanation: cows are vegetarian, once eat sheep's brains, thus it gone mad

> 2.2.1.2. What constraints does mad_cow inherit from its superclasses? Do you see any problem with that definition? Why?

- constraints: 
    - `eats only (not (animal))`
    - `eats only (not (part_of some animal))`
    - `eats some owl:Thing`
- A vegetarian is defined as an animal that eats no other animals, or parts of animals.
- Mad cows equivalent to `cow and (eats some (brain and (part_of some sheep)))`
    - Mad cows eat sheep's brain, this is a **violation**

#### 2.2.2 Reasoner

> 2.2.2.1. What happened to the definition of mad_cow? Compare with result when not using reasoner. (Hint: check also the class hierarchy (inferred) tab)

After use reasoner, on "class hierachy (inferred)" tab,  mad cow $\sqsubseteq$ owl:Nothing

> 2.2.2.2. What happened to the giraffe class? Compare with result when not using reasoner.

- After using reasoner, `Giraffe` becomes the subclass of `vegetarian` and gains the constraints from `vegetarian` as well.

> 2.2.2.3. Which classes do Tom and Minnie belong to? Compare with result when not using reasoner. (Hint: Minnie has_pet Tom).

|        | Tom                     | Minnie                        |
| ------ | ----------------------- | ----------------------------- |
| Before | `owl:Thing`             | `elderly` `female`            |
| After  | `owl:Thing` `cat` `pet` | `elderly` `female` `old lady` |

> 2.2.2.4. List all the person instances. Compare with result when not using reasoner. Which ones were added after you executed the reasoner? Describe why each of the additional instances were added.

Before: Fred, Joe, Kevin, Walt

After: Fred, Joe, Kevin, Walt and

- Mick: `dog owner` and `white van man`
- Minnie: `old lady`
- Pete: `pet owner`


> 2.2.2.5. Give a complete description of the instance Mick. Which classes do Daily Mirror belong to? Compare with result when not using reasoner.

|        | Mick                                                         | Daily Mirror                                   |
| ------ | ------------------------------------------------------------ | ---------------------------------------------- |
| Before | `male` *Mick is male and drives a white van*                 | `owl:Thing` *The paper read by Mick.*          |
| After  | `male` `dog owner` `white van man` *Mick is male and drives a white van* | `owl:Thing` `tabloid`*The paper read by Mick.* |

> 2.2.2.6. List all the descendant classes of pet owner.

- animal lower (after reasoning )
- cat owner (after reasoning )
- dog owner  (after reasoning )
- old lady (subClass of `(has_pet some animal) and (has_pet only cat)`)

> 2.2.2.7. How many “pets” must a person have to be considered an animal-lover?

3

> 2.2.2.8. Do all the “pets” of an animal-lover need to be animals? Does an “old lady” need to be a person?

- Yes. the ranges of `has_pet` is `animal`
- Yes, `old lady` <u>equivlant to</u> `elderly` and `female` and `person`




