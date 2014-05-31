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
#I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i C %{buildroot}/usr/lib/locale/C.UTF-8
I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i tr_TR %{buildroot}/usr/lib/locale/tr_TR.UTF-8
I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i et_EE %{buildroot}/usr/lib/locale/et_EE.UTF-8
I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i lt_LT %{buildroot}/usr/lib/locale/lt_LT.UTF-8
I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i uz_UZ %{buildroot}/usr/lib/locale/uz_UZ.UTF-8
I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i hy_AM %{buildroot}/usr/lib/locale/hy_AM.UTF-8
I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i vi_VN %{buildroot}/usr/lib/locale/vi_VN.UTF-8

# not supported :  kn_CA ml_MY ms_MW zh_CH
REGEX="(ar_AE|as_IN|az_AZ|bg_BG|ca_ES|cs_CZ|da_DK|de_AT|de_CH|de_DE|el_GR|en_AU|en_CA|en_GB|en_IE|en_NZ|en_PH|en_US|en_ZA|es_ES|es_MX|es_US|et_EE|eu_ES|fi_FI|fr_BE|fr_CA|fr_CH|fr_FR|ga_IE|gl_ES|he_IL|hr_HR|hu_HU|id_ID|is_IS|it_IT|iw_IL|ja_JP|ka_GE|kk_KZ|kn_CA|ko_KR|lt_LT|lv_LV|mk_MK|ml_MY|ms_MW|ms_MY|nb_NO|nl_BE|nl_NL|pl_PL|pt_BR|pt_PT|ro_RO|ru_RU|sk_SK|sl_SI|sq_AL|sv_SE|th_TH|tl_PH|tr_TR|uk_UA|zh_CH|zh_CN|zh_HK|zh_SG|zh_TW).*UTF-8"
for loc in  `grep -E $REGEX localedata/SUPPORTED | cut -d"." -f1`; do
  I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i $loc  %{buildroot}/usr/lib/locale/$loc.UTF-8
done
REGEX1="(bn_IN|fa_IR|fil_PH|gu_IN|hi_IN|km_KH|kn_IN|lo_LA|ml_IN|mr_IN|my_MM|ne_NP|or_IN|pa_IN|pa_PK|si_LK|sr_RS|ta_IN|te_IN|ur_PK)"
for loc1 in  `grep -E $REGEX1 localedata/SUPPORTED | cut -d"/" -f1`; do
  I18NPATH=localedata GCONV_PATH=iconvdata localedef --quiet -c -f UTF-8 -i $loc1  %{buildroot}/usr/lib/locale/$loc1
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
