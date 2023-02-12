CREATE VIEW Fastest_Events
AS
SELECT *
	FROM Fastest_Womens_Event
	GROUP BY category
UNION
SELECT * 
	FROM Fastest_Mens_Event
	GROUP BY category

