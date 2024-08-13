CREATE OR REPLACE PROCEDURE public.process_spotify_api_response(IN in_user_pk INTEGER, IN response jsonb)
LANGUAGE 'plpgsql'  -- Use 'plpgsql' for procedural SQL, not 'sql'
AS $BODY$
DECLARE
    item_obj jsonb;
BEGIN
    -- Iterate over each item in the JSONB array
    FOR item_obj IN 
        SELECT jsonb_array_elements(response->'items') AS item_obj
    LOOP

        CALL public.add_item_to_db(item_obj);

        -- SONG
        INSERT INTO spotify_history_listen_history(account_id, timestamp, song_id)
        VALUES (
            in_user_pk, 
            (item_obj->>'played_at')::timestamp, 
            (item_obj->'track'->>'id')::varchar
        )
        ON CONFLICT (account_id, timestamp) DO NOTHING; -- Optional: Prevents duplicates if id is unique

    END LOOP;
END;
$BODY$;
ALTER PROCEDURE public.process_spotify_api_response OWNER TO admin;
GRANT EXECUTE ON PROCEDURE public.process_spotify_api_response TO pg_write_all_data;
REVOKE ALL ON PROCEDURE public.process_spotify_api_response FROM PUBLIC;
COMMENT ON PROCEDURE public.process_spotify_api_response IS 'Deserialize item JSON and add selected metadata into database';