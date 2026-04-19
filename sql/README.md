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

/*
Q15. How can you output a list of all members who have recommended another member? Ensure that there are no duplicates in the list, and that results are ordered by (surname, firstname).
*/
SELECT DISTINCT M.firstname, M.surname 
	FROM cd.members AS M
	JOIN cd.members AS R
	ON 
	M.memid = R.recommendedby
	ORDER BY surname, firstname;

/*
Q16. How can you output a list of all members, including the individual who recommended them (if any), without using any joins? Ensure that there are no duplicates in the list, and that each firstname + surname pairing is formatted as a column and ordered.
*/

SELECT DISTINCT M.firstname || ' ' || M.surname AS member, 
	(SELECT R.firstname || ' ' || R.surname AS recommender 
	 	FROM cd.members as R
		WHERE R.memid = M.recommendedby
	)
	FROM cd.members AS M
ORDER BY member;

/*
Q16. Produce a count of the number of recommendations each member has made. Order by member ID.
*/

SELECT recommendedby, COUNT(*) FROM cd.members
	WHERE recommendedby IS NOT NULL
	GROUP BY recommendedby
ORDER BY recommendedby;

/*
Q17. Produce a count of the number of recommendations each member has made. Order by member ID.
*/

SELECT recommendedby, COUNT(*) FROM cd.members
	WHERE recommendedby IS NOT NULL
	GROUP BY recommendedby
ORDER BY recommendedby;

/*
Q17. Produce a list of the total number of slots booked per facility. For now, just produce an output table consisting of facility id and slots, sorted by facility id.
*/

SELECT facid, SUM(slots) FROM cd.bookings
  GROUP BY facid
ORDER BY facid

/*
Q18. Produce a list of the total number of slots booked per facility in the month of September 2012. Produce an output table consisting of facility id and slots, sorted by the number of slots.
*/

SELECT facid, SUM(slots) as "Total Slots" FROM cd.bookings
  WHERE starttime >= '2012-09-01' AND starttime < '2012-10-01'
  GROUP BY facid
  ORDER BY SUM(slots)

/*
Q19. Produce a list of the total number of slots booked per facility per month in the year of 2012. Produce an output table consisting of facility id and slots, sorted by the id and month.
*/

SELECT facid, EXTRACT(month FROM starttime) as month, SUM(slots) as "Total Slots"
FROM cd.bookings
WHERE EXTRACT(year FROM starttime) = 2012
  GROUP BY facid, month
ORDER BY facid, month

/*
Q19. Find the total number of members (including guests) who have made at least one booking.
*/

SELECT COUNT(distinct memid) FROM cd.bookings

/*
Q20. Produce a list of each member name, id, and their first booking after September 1st 2012. Order by member ID.
*/

SELECT m.surname, m.firstname, m.memid, min(b.starttime) FROM cd.members AS m 
JOIN cd.bookings as b
	ON m.memid = b.memid
	WHERE b.starttime >= '2012-09-01'
	GROUP BY m.surname, m.firstname, m.memid
ORDER BY m.memid

/*
Q21. Produce a list of member names, with each row containing the total member count. Order by join date, and include guest members.
*/

SELECT m.surname, m.firstname, m.memid, min(b.starttime) FROM cd.members AS m 
JOIN cd.bookings as b
	ON m.memid = b.memid
	WHERE b.starttime >= '2012-09-01'
	GROUP BY m.surname, m.firstname, m.memid
ORDER BY m.memid

/*
Q22. Produce a list of member names, with each row containing the total member count. Order by join date, and include guest members.
*/

SELECT COUNT(*) over(), firstname, surname FROM cd.members
ORDER BY joindate

/*
Q23. Output the facility id that has the highest number of slots booked. Ensure that in the event of a tie, all tieing results get output.
*/

select facid, total from (
	select facid, sum(slots) total, rank() over (order by sum(slots) desc) rank
        	from cd.bookings
		group by facid
	) as ranked
	where rank = 1

NOTE 
-> Group bookings by facility -> sum slots -> rank them -> return the top ones (including ties)”

/*
Q24. Output the names of all members, formatted as 'Surname, Firstname'
*/

SELECT (surname || ', ' || firstname)  as NAME FROM cd.members


/*
Q25. Output the names of all members, formatted as 'Surname, Firstname'
/*

SELECT memid, telephone FROM cd.members WHERE telephone ~ '[()]';
ORDER BY memid;

/*
Q26. You'd like to produce a count of how many members you have whose surname starts with each letter of the alphabet. Sort by the letter, and don't worry about printing out a letter if the count is 0.
/*

SELECT substr (m.surname,1,1) AS letter, COUNT(*) AS count 
    FROM cd.members m
    GROUP BY letter
    ORDER BY letter        














	

	
	
	


