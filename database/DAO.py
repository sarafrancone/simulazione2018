from database.DB_connect import DBConnect
from model.state import State


class DAO():

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct year(s.`datetime`) as year
                    from sighting s 
                    order by year(s.`datetime`) asc"""

        cursor.execute(query,)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAvvistamenti(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct count(*) as n
                    from sighting s 
                    where year(s.`datetime`)=%s"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(row["n"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodes(anno):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct s2.*
                    from sighting s, state s2 
                    where s.state = s2.id and year(s.`datetime`)=%s
                    group by s2.id"""

        cursor.execute(query,(anno,))

        for row in cursor:
            result.append(State(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getEdges(anno, keys):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct s1.state as s1, s2.state as s2
                    from sighting s1, sighting s2
                    where year(s2.`datetime`) = %s and year(s1.`datetime`) = %s
                    and s1.state<>s2.state 
                    and s2.`datetime` > s1.`datetime`
                    group by s1.state, s2.state """

        cursor.execute(query, (anno, anno,))

        for row in cursor:
            if row["s1"].upper() in keys and row["s2"].upper() in keys:
                result.append((row["s1"].upper(), row["s2"].upper()))

        cursor.close()
        conn.close()
        return result

