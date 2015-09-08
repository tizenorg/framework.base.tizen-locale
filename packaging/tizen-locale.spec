Name:   tizen-locale	
Summary: carring locale information for tizen platform
Version:0.1
Release:1
License:LGPLv2+ and LGPLv2+ with exceptions and GPLv2+
Group: 	System/Libraries

Source: %{name}-%{version}.tar.gz
Source10: generate-supported.mk
Source99: LICENSES

BuildRequires: eglibc-common
BuildRequires: tzdata >= 2003a
Requires: tzdata
Requires: eglibc-common

%description
carring locale information for tizen platform

%prep
%setup -q 

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT

mkdir -p %{buildroot}/%{_prefix}/share/license
install -m 644 %SOURCE99 $RPM_BUILD_ROOT/%{_prefix}/share/license/%{name}

mkdir -p %{buildroot}/usr/lib/locale


CHARSET=UTF-8
LOCALE_DIR=%{buildroot}/usr/lib/locale
mkdir -p $LOCALE_DIR

REGEX="(aa_DJ|aa_ER|aa_ET|af_ZA|am_ET|an_ES|ar_AE|ar_BH|ar_DZ|ar_EG|ar_IN|ar_IQ|ar_JO|ar_KW|ar_LB|ar_LY|ar_MA|ar_OM|ar_QA|ar_SA|ar_SD|ar_SY|ar_TN|ar_YE|as_IN|ast_ES|az_AZ|be_BY|ber_DZ|ber_MA|bg_BG|bn_BD|bn_IN|bo_CN|bo_IN|br_FR|bs_BA|byn_ER|ca_AD|ca_ES|ca_FR|ca_IT|crh_UA|csb_PL|cs_CZ|cv_RU|cy_GB|da_DK|de_AT|de_BE|de_CH|de_DE|de_LU|dv_MV|dz_BT|el_CY|el_GR|en_AG|en_AU|en_BW|en_CA|en_DK|en_GB|en_HK|en_IE|en_IN|en_NG|en_NZ|en_PH|en_SG|en_US|en_ZA|en_ZW|es_AR|es_BO|es_CL|es_CO|es_CR|es_DO|es_EC|es_ES|es_GT|es_HN|es_MX|es_NI|es_PA|es_PE|es_PR|es_PY|es_SV|es_US|es_UY|es_VE|et_EE|eu_ES|fa_IR|fi_FI|fil_PH|fo_FO|fr_BE|fr_CA|fr_CH|fr_FR|fr_LU|fur_IT|fy_DE|fy_NL|ga_IE|gd_GB|gez_ER|gez_ET|gl_ES|gu_IN|gv_GB|ha_NG|he_IL|hi_IN|hne_IN|hr_HR|hsb_DE|ht_HT|hu_HU|hy_AM|i18n|id_ID|ig_NG|ik_CA|is_IS|it_CH|it_IT|iu_CA|iw_IL|ja_JP|ka_GE|kk_KZ|kl_GL|km_KH|kn_IN|kok_IN|ko_KR|ks_IN|ku_TR|kw_GB|ky_KG|lg_UG|li_BE|li_NL|lo_LA|lt_LT|lv_LV|mai_IN|mg_MG|mi_NZ|mk_MK|ml_IN|mn_MN|mr_IN|ms_MY|mt_MT|my_MM|nb_NO|nds_DE|nds_NL|ne_NP|nl_AW|nl_BE|nl_NL|nn_NO|nr_ZA|nso_ZA|oc_FR|om_ET|om_KE|or_IN|pa_IN|pap_AN|pa_PK|pl_PL|POSIX|ps_AF|pt_BR|pt_PT|ro_RO|ru_RU|ru_UA|rw_RW|sa_IN|sc_IT|sd_IN|se_NO|shs_CA|sid_ET|si_LK|sk_SK|sl_SI|so_DJ|so_ET|so_KE|so_SO|sq_AL|sq_MK|sr_ME|sr_RS|ss_ZA|st_ZA|sv_FI|sv_SE|ta_IN|te_IN|tg_TJ|th_TH|ti_ER|ti_ET|tig_ER|tk_TM|tl_PH|tn_ZA|tr_CY|tr_TR|ts_ZA|tt_RU|ug_CN|uk_UA|ur_IN|ur_PK|uz_UZ|ve_ZA|vi_VN|wa_BE|wal_ET|wo_SN|xh_ZA|yi_US|yo_NG|zh_CN|zh_HK|zh_SG|zh_TW|zu_ZA)"
REGEX=`echo $REGEX | sed "s#\<en\>#en_GB#" | sed "s#\<[a-z]\+\>#&_.*#g"`

for LOCALE in `grep -E "^\<$REGEX\>.*/$CHARSET" localedata/SUPPORTED | cut -d '/' -f 1`
do
	I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f $CHARSET -i ${LOCALE%%.*} $LOCALE_DIR/$LOCALE
done

mkdir -p %{buildroot}/usr/share/i18n/
make -f %{SOURCE10} IN=localedata/SUPPORTED OUT=%{buildroot}/usr/share/i18n/SUPPORTED

%post -p /usr/sbin/build-locale-archive

%postun

%posttrans 
/bin/ls /usr/lib/locale/ | /bin/grep _ | /usr/bin/xargs -I {} /bin/rm -rf /usr/lib/locale/{}
/bin/rm -rf /usr/lib/locale/C.UTF-8
/bin/find /usr/share/locale/ -name libc.mo | /bin/grep -v en_GB | /usr/bin/xargs -I {} /bin/rm {}

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root)
%{_prefix}/lib/locale
%{_prefix}/share/license/%{name}
%attr(0644,root,root) %config %{_prefix}/share/i18n/SUPPORTED
%attr(0644,root,root) %verify(not md5 size mtime mode) %ghost %config(missingok,noreplace) %{_prefix}/lib/locale/locale-archive
%manifest tizen-locale.manifest
