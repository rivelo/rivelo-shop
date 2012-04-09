from django.conf.urls.defaults import *
from catalog.views import current_datetime, main_page
from catalog.test import current_datetime as curdate
from django.views.generic.simple import direct_to_template
from django.conf import settings

import os
dirname = os.path.dirname(globals()["__file__"])


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^search/$', 'catalog.accounting.views.search'), 
    (r'^contact/thanks/$', direct_to_template, {'template': 'thanks.html'}),
    (r'^contact/$', 'catalog.accounting.views.contact'),


    (r'^manyforms/(?P<author_id>\d+)$', 'catalog.accounting.views.manage_works'),
    (r'^manyforms/test/$', 'catalog.accounting.views.formset_test'),
    (r'^workshop/done/client/(?P<id>\d+)/$', 'catalog.accounting.views.formset_test'),
    (r'^manyforms/test1/$', 'catalog.accounting.views.inline_formset_test'),

    # Manufacturer operation
    (r'^manufacturer/search/$', 'catalog.accounting.views.search'), 
    (r'^manufacturer/view/$', 'catalog.accounting.views.manufaturer_list'), 
    (r'^manufacturer/add/$', 'catalog.accounting.views.manufacturer_add'),
    (r'^manufacturer/edit/(?P<id>\d+)/$', 'catalog.accounting.views.manufacturer_edit'),    
    (r'^manufacturer/delete/(?P<id>\d+)/$', 'catalog.accounting.views.manufacturer_delete'),

    # Country operation
    (r'^country/add/$', 'catalog.accounting.views.country_add'),
    (r'^country/view/$', 'catalog.accounting.views.country_list'),
    (r'^country/edit/(?P<id>\d+)/$', 'catalog.accounting.views.country_edit'),    
    (r'^country/delete/(?P<id>\d+)/$', 'catalog.accounting.views.country_delete'),
    #(r'^country/delete/(?P<id>\d)/$', 'catalog.accounting.views.dealer2_del'),

    # Bank operation
    (r'^bank/add/$', 'catalog.accounting.views.bank_add'),
    (r'^bank/view/$', 'catalog.accounting.views.bank_list'),
    (r'^bank/edit/(?P<id>\d+)/$', 'catalog.accounting.views.bank_edit'),    
    (r'^bank/delete/(?P<id>\d+)/$', 'catalog.accounting.views.bank_del'),

    # Bicycle operation
    (r'^bicycle-type/add/$', 'catalog.accounting.views.bicycle_type_add'),
    (r'^bicycle-type/view/$', 'catalog.accounting.views.bicycle_type_list'),
    (r'^bicycle-type/edit/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_type_edit'),    
    (r'^bicycle-type/delete/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_type_del'),

    (r'^bicycle-framesize/add/$', 'catalog.accounting.views.bicycle_framesize_add'),
    (r'^bicycle-framesize/view/$', 'catalog.accounting.views.bicycle_framesize_list'),
    (r'^bicycle/framesize/edit/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_framesize_edit'),    
    (r'^bicycle/framesize/delete/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_framesize_del'),
    #(r'^bicycle/framesize/delete/(?P<id>\d)/$', 'catalog.accounting.views.bicycle_framesize_del'),

    (r'^bicycle/add/$', 'catalog.accounting.views.bicycle_add'),
    (r'^bicycle/year/(?P<year>\d+)/view/$', 'catalog.accounting.views.bicycle_list'),
    (r'^bicycle/all/view/$', 'catalog.accounting.views.bicycle_all_list'),
    (r'^bicycle/view/$', 'catalog.accounting.views.bicycle_list'),
    (r'^bicycle/edit/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_edit'),    
    (r'^bicycle/delete/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_del'),
    (r'^bicycle/photo/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_photo'),

    (r'^bicycle/store/report/bysize/(?P<id>\d+)/$', 'catalog.accounting.views.store_report_bysize'),
    (r'^bicycle/store/report/bytype/(?P<id>\d+)/$', 'catalog.accounting.views.store_report_bytype'),
    (r'^bicycle/store/price/$', 'catalog.accounting.views.bicycle_store_price'),
    (r'^bicycle/store/price/print/$', 'catalog.accounting.views.bicycle_store_price_print'),    
    (r'^bicycle-store/add/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_store_add'),
    (r'^bicycle-store/add/$', 'catalog.accounting.views.bicycle_store_add'),
    (r'^bicycle-store/all/view/seller/$', 'catalog.accounting.views.bicycle_store_list_by_seller', {'all': True}),
    (r'^bicycle-store/view/seller/$', 'catalog.accounting.views.bicycle_store_list_by_seller'),
    (r'^bicycle-store/now/view/$', 'catalog.accounting.views.bicycle_store_list'),
    (r'^bicycle-store/all/view/$', 'catalog.accounting.views.bicycle_store_list',{'all': True}),
    (r'^bicycle-store/view/$', 'catalog.accounting.views.bicycle_store_list'),
    (r'^bicycle-store/edit/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_store_edit'),
    (r'^bicycle-store/delete/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_store_del'),
    (r'^bicycle-store/search/$', 'catalog.accounting.views.bicycle_store_search'),
    (r'^bicycle-store/search/result/$', 'catalog.accounting.views.bicycle_store_search_result'),

    (r'^bicycle/sale/add/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_sale_add'),
    (r'^bicycle/sale/add/$', 'catalog.accounting.views.bicycle_sale_add'),
    (r'^bicycle/sale/id/(?P<id>\d+)/view/$', 'catalog.accounting.views.bicycle_sale_list'),
    (r'^bicycle/sale/view/$', 'catalog.accounting.views.bicycle_sale_list'),
    (r'^bicycle/sale/year/(?P<year>\d+)/month/(?P<month>\d+)/view/$', 'catalog.accounting.views.bicycle_sale_list'),
    (r'^bicycle/sale/edit/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_sale_edit'),    
    (r'^bicycle/sale/delete/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_sale_del'),
    (r'^bicycle/sale/report/month/$', 'catalog.accounting.views.bicycle_sale_report'),
    (r'^bicycle/sale/service/(?P<id>\d+)/$', 'catalog.accounting.views.bicycle_sale_service'),
    # bicycle order by client
    (r'^bicycle/order/view/$', 'catalog.accounting.views.bicycle_order_list'),
    (r'^bicycle/order/add/$', 'catalog.accounting.views.bicycle_order_add'),
    (r'^bicycle/order/(?P<id>\d+)/delete/$', 'catalog.accounting.views.bicycle_order_del'),    
        
    # Dealer/Dealer Managers operation
    (r'^dealer/payment/add/$', 'catalog.accounting.views.dealer_payment_add'),
    (r'^dealer/payment/view/$', 'catalog.accounting.views.dealer_payment_list'),
    (r'^dealer/payment/delete/(?P<id>\d+)/$', 'catalog.accounting.views.dealer_payment_del'),

    (r'^dealer/invoice/add/$', 'catalog.accounting.views.dealer_invoice_add'),
    (r'^dealer/invoice/view/$', 'catalog.accounting.views.dealer_invoice_list_month'),
    (r'^dealer/invoice/year/(?P<year>\d+)/(?P<pay>paid|notpaid|sending)/$', 'catalog.accounting.views.dealer_invoice_list_month'),
    (r'^dealer/invoice/year/(?P<year>\d+)/month/(?P<month>\d+)/view/$', 'catalog.accounting.views.dealer_invoice_list_month'),
    #(r'^dealer/invoice/month/(?P<month>\d+)/view/$', 'catalog.accounting.views.dealer_invoice_list_month'),
    (r'^dealer/invoice/view/all/$', 'catalog.accounting.views.dealer_invoice_list'),
    (r'^dealer/invoice/view/$', 'catalog.accounting.views.dealer_invoice_list'),
    (r'^dealer/invoice/search/$', 'catalog.accounting.views.dealer_invoice_search'),
    (r'^dealer/invoice/search/result/$', 'catalog.accounting.views.dealer_invoice_search_result'),
    (r'^dealer/invoice/edit/(?P<id>\d+)/$', 'catalog.accounting.views.dealer_invoice_edit'),
    (r'^dealer/invoice/delete/(?P<id>\d+)/$', 'catalog.accounting.views.dealer_invoice_del'),
    
    (r'^dealer/add/$', 'catalog.accounting.views.dealer_add'),
    (r'^dealer/view/$', 'catalog.accounting.views.dealer_list'),
    (r'^dealer/edit/(?P<id>\d+)/$', 'catalog.accounting.views.dealer_edit'),
    (r'^dealer/delete/(?P<id>\d+)/$', 'catalog.accounting.views.dealer_del'),

    (r'^dealer-manager/add/$', 'catalog.accounting.views.dealer_manager_add'),
    (r'^dealer-manager/view/$', 'catalog.accounting.views.dealer_manager_list'),
    (r'^dealer-manager/edit/(?P<id>\d+)/$', 'catalog.accounting.views.dealer_manager_edit'),    
    (r'^dealer-manager/delete/(?P<id>\d+)/$', 'catalog.accounting.views.dealer_manager_del'),

    #Invoice
    (r'^invoice/add/$', 'catalog.accounting.views.invoicecomponent_add'),
    (r'^invoice/catalog/(?P<cid>\d+)/add/$', 'catalog.accounting.views.invoicecomponent_add'),
    (r'^invoice/manufacture/(?P<mid>\d+)/add/$', 'catalog.accounting.views.invoicecomponent_add'),
    (r'^invoice/manufacture/(?P<mid>\d+)/view/$', 'catalog.accounting.views.invoicecomponent_list_by_manufacturer'),
    (r'^invoice/manufacture/view/$', 'catalog.accounting.views.invoicecomponent_list_by_manufacturer'),
    (r'^invoice/category/view/$', 'catalog.accounting.views.invoicecomponent_list_by_category'),
    (r'^invoice/category/(?P<cid>\d+)/view/$', 'catalog.accounting.views.invoicecomponent_list_by_category'),
    (r'^invoice/list/(?P<limit>\d+)/view/$', 'catalog.accounting.views.invoicecomponent_list'),
    (r'^invoice/list/view/$', 'catalog.accounting.views.invoicecomponent_list'),
    (r'^invoice/id/(?P<id>\d+)/view/$', 'catalog.accounting.views.invoice_id_list'),
    (r'^invoice/catalog/(?P<cid>\d+)/view/$', 'catalog.accounting.views.invoice_cat_id_list'),
    (r'^invoice/delete/(?P<id>\d+)/$', 'catalog.accounting.views.invoicecomponent_del'),
    (r'^invoice/edit/(?P<id>\d+)/$', 'catalog.accounting.views.invoicecomponent_edit'),
    (r'^invoice/report/$', 'catalog.accounting.views.invoice_report'),
    (r'^invoice/all/report/$', 'catalog.accounting.views.invoicecomponent_sum'),
    (r'^invoice/test/$', 'catalog.accounting.views.invoicecomponent_tets'),
    (r'^invoice/search/$', 'catalog.accounting.views.invoice_search'),
    (r'^invoice/search/result/$', 'catalog.accounting.views.invoice_search_result'),
    

    # Curency operation
    (r'^curency/add/$', 'catalog.accounting.views.curency_add'),
    (r'^curency/view/$', 'catalog.accounting.views.curency_list'),
    (r'^curency/delete/(?P<id>\d+)/$', 'catalog.accounting.views.curency_del'),
    
    (r'^exchange/add/$', 'catalog.accounting.views.exchange_add'),
    (r'^exchange/view/$', 'catalog.accounting.views.exchange_list'),
    (r'^exchange/edit/(?P<id>\d+)/$', 'catalog.accounting.views.exchange_edit'),
    (r'^exchange/delete/(?P<id>\d+)/$', 'catalog.accounting.views.exchange_del'),

    # Component Type operation
    (r'^category/add/$', 'catalog.accounting.views.category_add'),
    (r'^category/view/$', 'catalog.accounting.views.category_list'),
    (r'^category/edit/(?P<id>\d+)$', 'catalog.accounting.views.category_edit'),
    (r'^category/delete/(?P<id>\d+)$', 'catalog.accounting.views.category_del'),    

    # Catalog operation
    (r'^catalog/add/$', 'catalog.accounting.views.catalog_add'),
    #(r'^catalog/change/$', 'catalog.accounting.views.catalog_tresult'),
    (r'^catalog/discount/$', 'catalog.accounting.views.catalog_discount_list'),
    (r'^catalog/id/(?P<id>\d+)/view/$', 'catalog.accounting.views.catalog_list'),
    (r'^catalog/view/$', 'catalog.accounting.views.catalog_list'),
    (r'^catalog/manufacture/(?P<id>\d+)/type/(?P<tid>\d+)/view/$', 'catalog.accounting.views.catalog_manu_type_list'),
    (r'^catalog/manufacture/(?P<id>\d+)/view/(\d+)$', 'catalog.accounting.views.catalog_part_list'),
    (r'^catalog/manufacture/(?P<id>\d+)/view/$', 'catalog.accounting.views.catalog_manufacture_list'),
    (r'^catalog/manufacture/view/$', 'catalog.accounting.views.catalog_manufacture_list'),
    (r'^catalog/type/(?P<id>\d+)/view/$', 'catalog.accounting.views.catalog_type_list'),    
    (r'^catalog/edit/(?P<id>\d+)$', 'catalog.accounting.views.catalog_edit'),
    (r'^catalog/delete/(?P<id>\d+)$', 'catalog.accounting.views.catalog_delete'),
    (r'^catalog/search/$', 'catalog.accounting.views.catalog_search'),
    (r'^catalog/search/id/$', 'catalog.accounting.views.catalog_search_id'),
    (r'^catalog/search/result/$', 'catalog.accounting.views.catalog_search_result'),

    # Client
    (r'^client/(?P<id>\d+)$', 'catalog.accounting.views.client_data'),
    (r'^clients/balance/$', 'catalog.accounting.views.client_balance_list'),
    (r'^client/add/$', 'catalog.accounting.views.client_add'),
    (r'^client/edit/(?P<id>\d+)$', 'catalog.accounting.views.client_edit'),
    (r'^client/view/$', 'catalog.accounting.views.client_list'),
    (r'^client/delete/(?P<id>\d+)$', 'catalog.accounting.views.client_delete'),
    (r'^client/search/$', 'catalog.accounting.views.client_search'),
    (r'^client/search/result/$', 'catalog.accounting.views.client_search_result'),
    (r'^client/result/search/$', 'catalog.accounting.views.client_result'),
    (r'^client/result/$', 'catalog.accounting.views.search_client_id'),
    (r'^client/invoice/view/$', 'catalog.accounting.views.client_invoice_view'),
    (r'^client/invoice/(?P<id>\d+)/edit/$', 'catalog.accounting.views.client_invoice_edit'),
    (r'^client/(?P<cid>\d+)/invoice/add/$', 'catalog.accounting.views.client_invoice'),
    (r'^client/invoice/catalog/(?P<cid>\d+)/add/$', 'catalog.accounting.views.client_invoice'),
    (r'^client/invoice/catalog/(?P<id>\d+)/view/$', 'catalog.accounting.views.client_invoice_id'),
    (r'^client/invoice/add/$', 'catalog.accounting.views.client_invoice'),
    (r'^client/invoice/(?P<id>\d+)/delete/$', 'catalog.accounting.views.client_invoice_delete'),
    (r'^client/invoice/year/(?P<year>\d+)/month/(?P<month>\d+)/view/$', 'catalog.accounting.views.client_invoice_view', {'day': "all"}),
    (r'^client/invoice/year/(?P<year>\d+)/month/(?P<month>\d+)/day/(?P<day>\d+)/view/$', 'catalog.accounting.views.client_invoice_view'),

    (r'^clientdebts/add/(?P<id>\d+)$', 'catalog.accounting.views.clientdebts_add'),
    (r'^clientdebts/view/$', 'catalog.accounting.views.clientdebts_list'),
    (r'^clientdebts/edit/(?P<id>\d+)$', 'catalog.accounting.views.clientdebts_edit'),
    (r'^clientdebts/delete/(?P<id>\d+)$', 'catalog.accounting.views.clientdebts_delete'),

    (r'^clientcredits/add/(?P<id>\d+)$', 'catalog.accounting.views.clientcredits_add'),
    (r'^clientcredits/view/$', 'catalog.accounting.views.clientcredits_list'),
    (r'^clientcredits/edit/(?P<id>\d+)$', 'catalog.accounting.views.clientcredits_edit'),    
    (r'^clientcredits/delete/(?P<id>\d+)$', 'catalog.accounting.views.clientcredits_delete'),

    # WorkShop 
    #operation by GROUP
    (r'^workgroup/add/$', 'catalog.accounting.views.workgroup_add'),
    (r'^workgroup/edit/(?P<id>\d+)$', 'catalog.accounting.views.workgroup_edit'),
    (r'^workgroup/view/$', 'catalog.accounting.views.workgroup_list'),
    (r'^workgroup/delete/(?P<id>\d+)$', 'catalog.accounting.views.workgroup_delete'),

    (r'^worktype/add/$', 'catalog.accounting.views.worktype_add'),
    (r'^worktype/edit/(?P<id>\d+)$', 'catalog.accounting.views.worktype_edit'),
    (r'^worktype/view/group/(?P<id>\d+)$', 'catalog.accounting.views.worktype_list'),        
    (r'^worktype/view/$', 'catalog.accounting.views.worktype_list'),
    (r'^worktype/delete/(?P<id>\d+)$', 'catalog.accounting.views.worktype_delete'),    

    (r'^workstatus/add/$', 'catalog.accounting.views.workstatus_add'),
    (r'^workstatus/view/$', 'catalog.accounting.views.workstatus_list'),
    (r'^workstatus/edit/(?P<id>\d+)$', 'catalog.accounting.views.workstatus_edit'),
    (r'^workstatus/delete/(?P<id>\d+)$', 'catalog.accounting.views.workstatus_delete'),

    (r'^workticket/add/$', 'catalog.accounting.views.workticket_add'),
    (r'^workticket/add/client/(?P<id>\d+)/$', 'catalog.accounting.views.workticket_add'),    
    (r'^workticket/view/$', 'catalog.accounting.views.workticket_list'),
    (r'^workticket/edit/(?P<id>\d+)/$', 'catalog.accounting.views.workticket_edit'),
    (r'^workticket/delete/(?P<id>\d+)/$', 'catalog.accounting.views.workticket_delete'),
    (r'^workticket/year/(?P<year>\d+)/month/(?P<month>\d+)/view/$', 'catalog.accounting.views.workticket_list'),
    (r'^workticket/all/view/$', 'catalog.accounting.views.workticket_list', {'all': True}),

    (r'^workshop/add/(?P<id>\d+)/$', 'catalog.accounting.views.workshop_add'),
    (r'^workshop/add/$', 'catalog.accounting.views.workshop_add'),
    (r'^workshop/edit/(?P<id>\d+)/$', 'catalog.accounting.views.workshop_edit'),
    (r'^workshop/view/$', 'catalog.accounting.views.workshop_list'),
    (r'^workshop/year/(?P<year>\d+)/month/(?P<month>\d+)/day/(?P<day>\d+)/view/$', 'catalog.accounting.views.workshop_list'),
    (r'^workshop/year/(?P<year>\d+)/month/(?P<month>\d+)/view/$', 'catalog.accounting.views.workshop_list', {'day': "all"}),
    (r'^workshop/year/(?P<year>\d+)/view/$', 'catalog.accounting.views.workshop_list'),
    (r'^workshop/delete/(?P<id>\d+)/$', 'catalog.accounting.views.workshop_delete'),    

    (r'^shop/sale/day/add/$', 'catalog.accounting.views.shopdailysales_add'),
    (r'^shop/sale/day/edit/(?P<id>\d+)/$', 'catalog.accounting.views.shopdailysales_edit'),
    (r'^shop/sale/view/month/(\d+)/$', 'catalog.accounting.views.shopdailysales_list'),
    (r'^shop/sale/view/$', 'catalog.accounting.views.shopdailysales_list'),
    (r'^shop/sale/day/(?P<id>\d+)/delete/$', 'catalog.accounting.views.shopdailysales_delete'),
    (r'^shop/price/lastadded/(?P<id>\d+)/view/$', 'catalog.accounting.views.shop_price_lastadd'),    
    (r'^shop/price/lastadded/(?P<id>\d+)/print/$', 'catalog.accounting.views.shop_price_lastadd_print'),
    (r'^shop/price/company/(?P<id>\d+)/view/$', 'catalog.accounting.views.shop_price'),
    (r'^shop/price/company/(?P<id>\d+)/print/$', 'catalog.accounting.views.shop_price_print'),
    (r'^shop/price/bysearch_id/(?P<id>.*)/view/$', 'catalog.accounting.views.shop_price_bysearch_id'),
    (r'^shop/price/bysearch_id/(?P<id>.*)/print/$', 'catalog.accounting.views.shop_price_bysearch_id_print'),
    (r'^shop/price/bysearch_name/(?P<id>.*)/view/$', 'catalog.accounting.views.shop_price_bysearch_name'),
    (r'^shop/price/bysearch_name/(?P<id>.*)/print/$', 'catalog.accounting.views.shop_price_bysearch_name_print'),
    
    # my cost
    (r'^cost/type/add/$', 'catalog.accounting.views.costtype_add'),
    (r'^cost/type/view/$', 'catalog.accounting.views.costtype_list'),
    (r'^cost/type/delete/(?P<id>\d+)$', 'catalog.accounting.views.costtype_delete'),    

    (r'^cost/add/(?P<id>\d+)$', 'catalog.accounting.views.cost_add'),
    (r'^cost/add/$', 'catalog.accounting.views.cost_add'),
    (r'^cost/view/$', 'catalog.accounting.views.cost_list'),
    (r'^cost/delete/(?P<id>\d+)/$', 'catalog.accounting.views.cost_delete'),    
    (r'^cost/edit/(?P<id>\d+)/$', 'catalog.accounting.views.cost_edit'),


    (r'^preorder/add/$', 'catalog.accounting.views.preorder_add'),
    (r'^preorder/view/$', 'catalog.accounting.views.preorder_list'),
    (r'^preorder/edit/(?P<id>\d+)/$', 'catalog.accounting.views.preorder_edit'),
    (r'^preorder/delete/(?P<id>\d+)/$', 'catalog.accounting.views.preorder_delete'),


    # Example:
    # (r'^catalog/', include('catalog.foo.urls')),

    (r'^media/(?P<path>.*)', 'django.views.static.serve',
     # static files
    #{'document_root': 'D:/develop/catalog/media'}),
    {'document_root': os.path.join(dirname, 'media')}),
    
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^admin/(.*)', admin.site.root),
    (r'^$', main_page),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^debuginfo$', 'catalog.views.debug'),
    )

