#for X in "en_GBR_dailyt_int" "en_NGA_thiday_int" "es_ARG_nacion_int" "es_MEX_jormex_int" "fr_DZA_xpress_int" "en_GBR_guardi_int" "en_NZL_nzhera_int" "es_BOL_larazo_int" "es_MEX_univer_int" "fr_FRA_lepari_int" "en_AUS_austra_int" "en_IND_hindti_int" "en_PAK_newint_int" "es_BOL_patria_int" "es_VEN_univer_int" "fr_FRA_lmonde_int" "en_AUS_hersun_int" "en_IND_tindia_int" "en_SGP_twoday_int" "es_CHL_mercur_int" "fr_BEL_derheu_int" "en_CAN_starca_int" "en_JPN_jatime_int" "en_USA_nytime_int" "es_CHL_tercer_int" "fr_BEL_lesoir_int" "en_CHN_chinad_int" "en_MLT_tmalta_int" "en_USA_wapost_int" "es_ESP_catalu_int" "fr_CAN_jmontr_int" "en_CHN_mopost_int" "en_MYS_starmy_int" "en_ZWE_chroni_int" "es_ESP_elpais_int" "fr_DZA_elwata_int"; do 
#X=""
#X="{es_ARG,es_BOL,es_CHL,es_MEX,es_VEN}*"
#X="es_*"
#X="es_ESP_*"
#X="es_[!E]*"
#X="fr_*"
#X="fr_FRA_*"
#X="fr_[!F]*"
#X="en_USA_*"
X="en_CHN_*"
./analyze.py '2014-01-01 00:00:00' '2014-02-01 00:00:00' $X 
./analyze.py '2014-02-01 00:00:00' '2014-03-01 00:00:00' $X
./analyze.py '2014-03-01 00:00:00' '2014-04-01 00:00:00' $X
./analyze.py '2014-04-01 00:00:00' '2014-05-01 00:00:00' $X
./analyze.py '2014-05-01 00:00:00' '2014-06-01 00:00:00' $X
./analyze.py '2014-06-01 00:00:00' '2014-07-01 00:00:00' $X
./analyze.py '2014-07-01 00:00:00' '2014-08-01 00:00:00' $X
./analyze.py '2014-08-01 00:00:00' '2014-09-01 00:00:00' $X
./analyze.py '2014-09-01 00:00:00' '2014-10-01 00:00:00' $X
./analyze.py '2014-10-01 00:00:00' '2014-11-01 00:00:00' $X
./analyze.py '2014-11-01 00:00:00' '2014-12-01 00:00:00' $X
./analyze.py '2014-12-01 00:00:00' '2015-01-01 00:00:00' $X
./analyze.py '2015-01-01 00:00:00' '2015-02-01 00:00:00' $X
./analyze.py '2015-02-01 00:00:00' '2015-03-01 00:00:00' $X
./analyze.py '2015-03-01 00:00:00' '2015-04-01 00:00:00' $X
./analyze.py '2015-04-01 00:00:00' '2015-05-01 00:00:00' $X
./analyze.py '2015-05-01 00:00:00' '2015-06-01 00:00:00' $X
./analyze.py '2015-06-01 00:00:00' '2015-07-01 00:00:00' $X
./analyze.py '2014-01-01 00:00:00' '2015-07-01 00:00:00' $X
done;
