# Task 1 Apache Jena

## 1.1

>Get names of actors whose name starts with the letter 'T', and the names of films they starred in (total of 2 columns).

Execution result:
<img src="./result/1.1.png" alt="1.1"  />

## 1.2

>Get URIs and names of **actors** who are also **writers** but are not **producers** (total of 2columns).

While I'm pretty sure different people can have duplicate names, there's no way I can differentiate between them. So for people with the same name, I can only assume it's the same person.

Execution result:
![1.2](./result/1.2.png)



## 1.3

> Get names of actors who starred in more than 18 films with the same director (who is not the actor). Show the name of the director and the number of films as well (total of 3 columns).

Execution result:
![1.3](./result/1.3.png)

## 1.4
> Get the names of countries, the number of comedy films (films with genre “Comedy”) and the population (in millions) for each country. The results should be sorted by the number of comedy films in descending order (total of 3 columns).

I only counted the number of `comedy` movies, other kind of comedy like `romantic comedy`,` Screwball comedy`, etc. are not included.

There are more than 200 countries or regions in `lmdb.nt`,  but only  a couple dozen countries have comedy movies. Since we need "number of comedy films", I will not ouput country without a comedy movie.

Execution result:
![1.4](./result/1.4.png)

## 1.5
>Get the names of female actors who were born after 1970 but before 1980. Show their date of birth (total of 2 columns).

> • Note that you do not have the data about gender and date-of-birth for actors in the provided graph. You will need to retrieve these values from an additional SPARQL endpoint using a federated query extension (the SERVICE keyword, read more about it here: https://www.w3.org/TR/sparql11-federated-query/).

Execution result:
![1.5](./result/1.5.png)


# Task 2 Wikidata

## 2.1

> Get URIs and names of actors who are also musicians and were part of (P361) a band sometime between 1960 to 2010. Also, show their date of birth. If an actor doesn't have date of birth, the value can be null, empty string, or missing (total of 3 columns).

My approach is limited by the information that provided by Wikidata, in that I am directly pulling the artist's time joined in a band from the artist page , If Wikidata only provides the start and end dates of the band, but not when the artist joined, then I will ignore the artist.

Complying with the requirements [here](https://blackboard.usc.edu/webapps/discussionboard/do/message?action=list_messages&course_id=_259094_1&nav=discussion_board&conf_id=_337946_1&forum_id=_222236_1&message_id=_2952262_1), if the time is exactly 1960 or exactly 2010, I did not count.

I've noticed that certain artists have more than one `date of birth` information. For this kind of artist, there will be more than one record that appears in the results.

Execution result:

![2.1](./result/2.1.png)

## 2.2

> Get URIs and names of films that include at least 4 cast members (P161) who have been nominated after the year 2000 for the Academy Award for Best Actor (Q103916). Also, show the number of such actors for each film (total of 3 columns).

Not all `point of time`  qualifier are provided under the "nominated for " property. Each Academy Awards instance did not provide nomination information either. Thus the number of my query result my may lower than reality.

Execution result:

![2.2](./result/2.2.png)