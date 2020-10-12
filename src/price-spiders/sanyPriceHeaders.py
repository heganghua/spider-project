# -*- coding: utf-8 -*-
"""
@author:华仔
@file: sanyPriceHeaders.py
@time: 2019/12/19
"""

import json

class Headers(object):

    def init(self):
        pass

    data = {
        "htmlbevt_ty": "htmlb:button:click:0",
        "htmlbevt_frm": "myFormId",
        "htmlbevt_oid": "C14_W48_V52_V51_BTN_SEARCH",
        "htmlbevt_id": "SEARCH",
        "htmlbevt_cnt": "0",
        "onInputProcessing": "htmlb",
        "SVH_INPUTFIELD_ID": "C14_W48_V52_V51_searchnode_parameters[2].VALUE1",
        "SVH_INPUTFIELD_VALUE": "",
        "thtmlbModifiedInputfieldIds": "C14_W48_V52_V51_searchnode_parameters[2].VALUE1==ZZCNDSRCH_ADVCNDRECSEARCHVIEW_物料编码",
        "sap-htmlb-design": "",
        "sap-ajaxtarget": "C1_W1_V2_C1_W1_V2_V3_C14_W48_V52_C14_W48_V52_V51_advcndrecsearchview.do",
        "sap-ajax_dh_mode": "AUTO",
        "wcf-secure-id": "783956CA21609FCFC82CE0341B60DEFA",
        "thtmlbKeyboardFocusId": "C14_W48_V52_V51_BTN_SEARCH",
        "thtmlbKeyboardSelectId": "",
        "AutoSaveFlag": "",
        "C11_W36_V37_SearchMenuAnchor1": "UP",
        "C13_W42_V43_selected_key": "",
        "thtmlbSliderState": "",
        "th-navbar-state": "",
        "C6_W22_V23_RecentObjects_isExpanded": "yes",
        "crmFrwScrollXPos": "0",
        "crmFrwScrollYPos": "0",
        "crmFrwOldScrollXPos": "0",
        "crmFrwOldScrollYPos": "0",
        "flashIslandsAsString": "",
        "callbackFlashIslands": "/sap(bD1aSCZjPTgwMCZpPTEmZT1SRjlRUlU1SFdURTBYMTlmTmpSZk1UTTRBRkJXdDJ2dkh0cXI3WDRrSHJKYmtRJTNkJTNk)/webcuif/uif_callback?crm_handler=CL_THTMLBX_FLASH_ISLAND&wcf-request-ticket=783956CA21609FCFC82CE0341B60DEFA",
        "silverlightIslandsAsString": "",
        "callbackSilverlightIslands": "/sap(bD1aSCZjPTgwMCZpPTEmZT1SRjlRUlU1SFdURTBYMTlmTmpSZk1UTTRBRkJXdDJ2dkh0cXI3WDRrSHJKYmtRJTNkJTNk)/webcuif/uif_callback?crm_handler=CL_THTMLBX_FLASH_ISLAND&wcf-request-ticket=783956CA21609FCFC82CE0341B60DEFA",
        "th-mes-isex": "",
        "C1_W1_V2_V3_V44_bchistory_selection": "",
        "C14_W48_V52_V51_advs0_advs_grps_state": "",
        "C14_W48_V52_V51_searchnode_parameters[1].FIELD": "KSCHL",
        "C14_W48_V52_V51_searchnode_parameters[1].operator": "EQ",
        "C14_W48_V52_V51_searchnode_parameters[1].VALUE1": "PR01",
        "C14_W48_V52_V51_searchnode_parameters[1].VALUE2": "0PI1",
        "C14_W48_V52_V51_searchnode_parameters[2].FIELD": "PRODUCT_ID",
        "C14_W48_V52_V51_searchnode_parameters[2].operator": "EQ",
        "C14_W48_V52_V51_searchnode_parameters[2].value1": "11016491",
        "C14_W48_V52_V51_searchnode_parameters[2].value2": "",
        "C14_W48_V52_V51_searchnode_parameters[3].FIELD": "VALID_ON",
        "C14_W48_V52_V51_searchnode_parameters[3].operator": "EQ",
        "C14_W48_V52_V51_searchnode_parameters[3].value1": "26.04.2020",
        "C14_W48_V52_V51_searchnode_parameters[3].value2": "",
        "C14_W48_V52_V51_searchnode_parameters[4].FIELD": "KVEWE",
        "C14_W48_V52_V51_searchnode_parameters[4].operator": "EQ",
        "C14_W48_V52_V51_searchnode_parameters[4].VALUE1": "PR",
        "C14_W48_V52_V51_searchnode_parameters[4].VALUE2": "PR",
        "C14_W48_V52_V51_searchnode_parameters[5].FIELD": "BILL_ORG",
        "C14_W48_V52_V51_searchnode_parameters[5].operator": "EQ",
        "C14_W48_V52_V51_searchnode_parameters[5].value1": "",
        "C14_W48_V52_V51_searchnode_parameters[5].value2": "",
        "C16_W56_V57_layout_include_layout": "",
        "C15_W49_V55_tv1_editMode": "NONE",
        "C15_W49_V55_tv1_isCellerator": "TRUE",
        "C15_W49_V55_tv1_selectedRows": "",
        "C15_W49_V55_tv1_rowCount": "1",
        "C15_W49_V55_tv1_lastSelectedRow": "",
        "C15_W49_V55_tv1_visibleFirstRow": "1",
        "C15_W49_V55_tv1_scrollPosition": "",
        "C15_W49_V55_tv1_hscrollPosition": "0",
        "C15_W49_V55_tv1_bindingString": "//CondRecList/Table",
        "C15_W49_V55_tv1_fixedColumns": "",
        "C15_W49_V55_tv1_filterApplied": "FALSE",
        "C15_W49_V55_tv1_firstSelectedRow": "",
        "C15_W49_V55_tv1_ctrlShiftKeyMode": "",
        "C15_W49_V55_tv1_previousSelectedRange": "",
        "C15_W49_V55_tv1_isNavModeActivated": "TRUE",
        "C15_W49_V55_tv1_tableIsFiltered": "",
        "C15_W49_V55_tv1_filterActionTriggered": "",
        "C15_W49_V55_tv1_sortActionTriggered": "",
        "C15_W49_V55_tv1_fixedColumnTriggered": "",
        "C15_W49_V55_tv1_firstTimeRendering": "NO",
        "C15_W49_V55_tv1_configHash": "3B23DE101D6FE3F157F1BB0FBDA949C2AE2745A2",
        "RESULT_LIST_CONFIG_KEY": "Z_SERVICE////CRMCMP_CND////<DEFAULT>////<DEFAULT>////CRMCMP_CND////CondRecListView",
        "C15_W49_V55_tv1_multiParameter": "0////0////0////0",
        "C15_W51_V55_hidenode_HIDEFIELDS": "true",
        "thtmlbScrollAreaWidth": "0",
        "thtmlbScrollAreaHeight": "0",
        "LTX_PREFIX_ID": "C1_W1_V2_",
        "C1_W1_V2_LTX_VETO_FLAG": "",
        "C1_W1_V2_ACTION_GUID": "",
        "C1_W1_V2_AC_OBJECT_KEY": "",
        "C1_W1_V2_AC_VALUE": "",
        "C1_W1_V2_AC_CONTAINER": "",
        "C1_W1_V2_MYITSLOCATION": "",
        "sap-ajax_request": "X"
    }

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Length': '3757',
        'Content-type': 'application/x-www-form-urlencoded',
        'Host': 'crmprd.sanygroup.com:8443',
        'Origin': 'https://crmprd.sanygroup.com:8443',
        # 'Referer': 'https://crmprd.sanygroup.com:8443/sap(ZT1SRjlRUlU1SFdURTBYMTlmTmpSZk1UTTRBRkJXdEYzRUh1cWg2MEtXYmZ4YzBRPT0=)/bc/bsp/sap/crm_ui_frame/BSPWDApplication.do?sap-client=800&sap-language=ZH&sap-domainrelax=min&sap-domainrelax=min',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    cookies = {}
    with open(r"cookies.txt") as f:
        for line in f.read().split(';'):
            name, value = line.strip().split('=', 1)
            cookies[name] = value

    url = "https://crmprd.sanygroup.com:8443/sap(ZT1SRjlRUlU1SFdURTBYMTlmTmpSZk1UTTRBRkJXdDJ2dkh0cXI3WDRrSHJKYmtRPT0=)/bc/bsp/sap/crm_ui_frame/BSPWDApplication.do?sap-client=800&sap-language=ZH&sap-domainrelax=min&sap-domainrelax=min"
