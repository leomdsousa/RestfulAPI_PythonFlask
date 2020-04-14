def normalizePathParams(cidade=None
                        , nota_min=0
                        , nota_max=5
                        , diaria_min=0
                        , diaria_max=10000
                        , limit=50
                        , offset = 0
                        , **dados):
    if cidade:
        return {
            "cidade": cidade
            , "nota_min": nota_min
            , "nota_max": nota_max
            , "diaria_min": diaria_min
            , "diaria_max": diaria_max
            , "limit": limit
            , "offset": offset
        }
    return {
        "nota_min": nota_min
        , "nota_max": nota_max
        , "diaria_min": diaria_min
        , "diaria_max": diaria_max
        , "limit": limit
        , "offset": offset
    }

def normalizeSitePathParams(url=None
                        , limit=50
                        , offset = 0
                        , **dados):
    if url:
        return {
            "url": url
            , "limit": limit
            , "offset": offset
        }
    return {
        "limit": limit
        , "offset": offset
    }

consulta_hotel_com_cidade = "SELECT * FROM TB_HOTEIS \
            WHERE CIDADE = ? \
            AND NOTA >= ? AND NOTA <= ? \
            AND DIARIA >= ? AND DIARIA <= ? \
            AND LIMIT > ? \
            AND OFFSET < ?"

consulta_hotel_sem_cidade = "SELECT * FROM TB_HOTEIS \
            WHERE AND NOTA >= ? AND NOTA <= ? \
            AND DIARIA >= ? AND DIARIA <= ? \
            AND LIMIT > ? \
            AND OFFSET < ?"

consulta_site_com_url = "SELECT * FROM TB_HOTEIS \
            WHERE CIDADE = ? \
            AND NOTA >= ? AND NOTA <= ? \
            AND DIARIA >= ? AND DIARIA <= ? \
            AND LIMIT > ? \
            AND OFFSET < ?"

consulta_site_sem_url = "SELECT * FROM TB_HOTEIS \
            WHERE AND NOTA >= ? AND NOTA <= ? \
            AND DIARIA >= ? AND DIARIA <= ? \
            AND LIMIT > ? \
            AND OFFSET < ?"