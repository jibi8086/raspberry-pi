select Buses.bus_name,s1.stop_name as from_stop_name,t1.departure_time,s2.stop_name as to_stop_name,t2.arrival_time
   from buses
inner join  route  t1 on t1.bus_id = buses.id
inner join Stop s1 on s1.id = t1.stop_id
inner join route t2 on t2.bus_id = buses.id
inner join Stop s2 on s2.id = t2.stop_id
where Buses.bus_name in (select bus_name from Buses)
and s1.stop_name = 'aluva'
   and s2.stop_name = 'angamaly'
