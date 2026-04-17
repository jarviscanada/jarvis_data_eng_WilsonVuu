# Introduction

# SQL Queries

###### Table Setup (DDL)
```sql
/*
Q1. The club is adding a new facility - a spa. We need to add it into the facilities table. Use the following values:
facid: 9, Name: 'Spa', membercost: 20, guestcost: 30, initialoutlay: 100000, monthlymaintenance: 800.
*/

INSERT INTO cd.facilities
    (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
VALUES
    (9, 'Spa', 20, 30, 100000, 800);


/*
Q2. Let's try adding the spa to the facilities table again. This time, though, we want to automatically generate the value for the next facid, rather than specifying it as a constant. Use the following values for everything else:
Name: 'Spa', membercost: 20, guestcost: 30, initialoutlay: 100000, monthlymaintenance: 800.
*/

INSERT INTO cd.facilities(facid, Name, membercost, guestcost, initialoutlay, monthlymaintenance)
SELECT (SELECT MAX(facid) FROM cd.facilities) + 1,'Spa', 20, 30, 100000, 800


/*
Q3. We made a mistake when entering the data for the second tennis court. The initial outlay was 10000 rather than 8000: you need to alter the data to fix the error.
*/

UPDATE cd.facilities
SET initialoutlay = 10000
WHERE name = 'Tennis Court 2'


/*
Q4. We want to alter the price of the second tennis court so that it costs 10% more than the first one. Try to do this without using constant values for the prices, so that we can reuse the statement if we want to.
*/

UPDATE cd.facilities
	SET 
		membercost = (SELECT membercost *1.1 FROM cd.facilities WHERE facid = 0),
		guestcost = (SELECT guestcost *1.1 FROM cd.facilities WHERE facid = 0)
	WHERE cd.facilities.facid = 1;


/*
Q5. As part of a clearout of our database, we want to delete all bookings from the cd.bookings table. How can we accomplish this?
*/

DELETE FROM cd.bookings;


/*
Q6. We want to remove member 37, who has never made a booking, from our database. How can we achieve that?
*/

DELETE FROM cd.members
WHERE memid = 37;


/*
Q7. How can you produce a list of facilities that charge a fee to members, and that fee is less than 1/50th of the monthly maintenance cost? Return the facid, facility name, member cost, and monthly maintenance of the facilities in question.
*/

SELECT facid, name, membercost, monthlymaintenance
FROM cd.facilities
WHERE membercost < monthlymaintenance / 50.0
  AND membercost > 0;


/*
Q8. How can you produce a list of all facilities with the word 'Tennis' in their name?
*/

SELECT *
FROM cd.facilities
WHERE name LIKE '%Tennis%';


/*
Q9. How can you retrieve the details of facilities with ID 1 and 5? Try to do it without using the OR operator.
*/

SELECT *
FROM cd.facilities
WHERE facid IN (1, 5);


/*
Q10. How can you produce a list of members who joined after the start of September 2012? Return the memid, surname, firstname, and joindate of the members in question.
*/

SELECT memid, surname, firstname, joindate FROM cd.members
	WHERE joindate >= '2012-07-01'


/*
Q11.You, for some reason, want a combined list of all surnames and all facility names. Yes, this is a contrived example :-). Produce that list!
*/

SELECT surname FROM cd.members AS m
	UNION
	SELECT name FROM cd.facilities AS f


/*
Q12. How can you produce a list of the start times for bookings by members named 'David Farrell'?
*/

SELECT b.starttime FROM cd.bookings AS b
	JOIN cd.members AS m 
 		ON b.memid = m.memid
	WHERE
		m.firstname='David' 
		AND 
		m.surname='Farrell'; 


/*
Q13. How can you produce a list of the start times for bookings for tennis courts, for the date '2012-09-21'? Return a list of start time and facility name pairings, ordered by the time.
*/

SELECT b.starttime as start, f.name as name FROM cd.bookings AS b
	JOIN
		cd.facilities AS f ON
		b.facid = f.facid
	WHERE 
		f.name like '%Tennis Court%' 
		AND
		b.starttime >='2012-09-21'
		AND
		b.starttime < '2012-09-22'
ORDER BY b.starttime ASC

/*
Q14. How can you output a list of all members, including the individual who recommended them (if any)? Ensure that results are ordered by (surname, firstname).
*/

SELECT m.firstname AS memfname, m.surname AS memsname, a.firstname AS recfname,a.surname AS recsname FROM cd.members as m
	LEFT OUTER JOIN cd.members AS a ON
	m.recommendedby = a.memid
	ORDER BY memsname, memfname;
	

	
	
	


