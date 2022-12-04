SELECT name, sum(strftime('%s', '0'||total_time) - strftime('%s','00:00:00')) seconds
FROM
	(SELECT RBEligible.name, eventresult.total_time, row_number() OVER (PARTITION BY name ORDER BY total_time ASC) AS fastest
	FROM 
		(SELECT rider.name, rider.rider_id, rider.isFemale, rider.isJunior, COUNT(rider.name) Ridden
		FROM eventresult 
		INNER JOIN rider ON rider.rider_id = eventresult.rider_id
		WHERE (eventresult.laps_completed = 11 AND eventresult.category LIKE '%RB%')
		GROUP BY rider.name
		HAVING Ridden > 5
		ORDER BY Ridden DESC ) As RBEligible
	INNER JOIN eventresult ON eventresult.rider_id = RBEligible.rider_id
	ORDER BY name, total_time)
WHERE fastest <= 6
GROUP BY name
ORDER BY seconds