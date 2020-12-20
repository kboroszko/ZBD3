START TRANSACTION ISOLATION LEVEL REPEATABLE READ;

do
$$
    declare
        p         record;
        paczka_id int;
        pozostalo record;
        znalazlem boolean := FALSE;
        slodycz varchar := 'asda';
        ilosc int := 10;
    begin
        INSERT INTO paczka (kraj, opis) VALUES ('Polska', 'bla bla bla') RETURNING id INTO paczka_id;
        SELECT ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa = slodycz INTO pozostalo;
        IF pozostalo.ilosc_pozostalych IS NULL THEN
            RAISE EXCEPTION 'FAIL! SLODYCZ NOT IN MAGAZYN';
        end if;
        raise notice 'znalazlem % %',pozostalo.ilosc_pozostalych,slodycz;
        IF pozostalo.ilosc_pozostalych < ilosc THEN
            raise notice 'szukam podobnego';
            for p in select podobny_do from podobny_slodycz where ktory_slodycz = slodycz order by podobny_do desc
                loop
                    raise notice 'counter: %', p.podobny_do;
                    SELECT ilosc_pozostalych FROM slodycz_w_magazynie WHERE nazwa = p.podobny_do INTO pozostalo;
                    IF not pozostalo.ilosc_pozostalych < ilosc THEN
                        znalazlem := TRUE;
                        slodycz := p.podobny_do;
                        raise notice 'znalazlem: %', p.podobny_do;
                        EXIT;
                    end if;
                end loop;
        else
            znalazlem := TRUE;
        end if;

        if znalazlem then
            raise notice 'SUKCES!!';
            raise notice 'biore %',slodycz;
            INSERT INTO slodycz_w_paczce VALUES (paczka_id, slodycz, ilosc);
            UPDATE slodycz_w_magazynie SET ilosc_pozostalych = ilosc_pozostalych - ilosc WHERE nazwa=slodycz;
        else
            raise EXCEPTION 'FAIL!!';
        end if;
    end;

$$;

COMMIT;