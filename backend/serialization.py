# from django.contrib.auth.models import User
# from django.core.serializers import serialize
# from rest_framework import serializers

# from backend.models import QuotationAirFreight, QuotationExportImportHandlingDetail, \
#     QuotationOtherCost, QuotationExportImportHandling, QuotationSupervisor, QuotationRecipient, \
#     Quotation, TemplateQuotation, Currency, Customer, CustomerContact


# class QuotationCustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = ('id', 'name', 'address', 'phone_number', 'mobile_phone')


# class QuotationCurrencySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Currency
#         fields = ('id', 'name')


# class QuotationTemplateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TemplateQuotation
#         fields = ('id', 'template_text', 'name', 'quotation_type')


# class QuotationAirFreightSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = QuotationAirFreight
#         fields = ('id', 'dest_or_origin', 'rates_min', 'rates_min_45', 'rates_plus_45',
#                   'rates_plus_100', 'rates_plus_300', 'rates_plus_500', 'rates_plus_1000',
#                   'fsc', 'ssc', 'route', 'service')


# class QuotationExportImportHandlingDetailSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = QuotationExportImportHandlingDetail
#         fields = '__all__'


# class QuotationOtherCostSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = QuotationOtherCost
#         fields = ('id', 'description', 'rates')


# class QuotationExportImportHandlingSerializer(serializers.ModelSerializer):

#     quotationexportimporthandlingdetail_set = QuotationExportImportHandlingDetailSerializer(
#         many=True)

#     class Meta:
#         model = QuotationExportImportHandling
#         fields = '__all__'


# class QuotationUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'email', 'first_name', 'last_name')


# class QuotationSupervisorSerializer(serializers.ModelSerializer):

#     user = QuotationUserSerializer(many=False)

#     class Meta:
#         model = QuotationSupervisor
#         fields = '__all__'


# class QuotationCustomerContactSerializer(serializers.ModelSerializer):

#     user = QuotationUserSerializer(many=False)

#     class Meta:
#         model = CustomerContact
#         fields = '__all__'

# class QuotationRecipientSerializer(serializers.ModelSerializer):

#     customer_contact = QuotationCustomerContactSerializer(many=False)

#     class Meta:
#         model = QuotationRecipient
#         fields = '__all__'


# class QuotationSerializer(serializers.ModelSerializer):

#     quotationairfreight_set = QuotationAirFreightSerializer(many=True)
#     quotationothercost_set = QuotationOtherCostSerializer(many=True)
#     quotationexportimporthandling_set = QuotationExportImportHandlingSerializer(many=True)
#     quotationsupervisor_set = QuotationSupervisorSerializer(many=True)
#     quotationrecipient_set = QuotationRecipientSerializer(many=True)
#     template_quotation = QuotationTemplateSerializer(many=False)
#     currency = QuotationCurrencySerializer(many=False)
#     customer = QuotationCustomerSerializer(many=False)

#     class Meta:
#         model = Quotation