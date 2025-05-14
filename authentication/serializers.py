from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from authentication.models import CustomUser, PersonalProfile, OrganisationProfile, InvestorProfile



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['account_type'] = user.account_type
        return token
    


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    account_type = serializers.ChoiceField(choices=CustomUser.ACCOUNT_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username','email', 'password', 'confirm_password', 'account_type']


    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        account_type = validated_data.pop('account_type')
        user = CustomUser.objects.create_user(**validated_data)
    
        #Corrsponding profile
        if account_type == 'investor':
            InvestorProfile.objects.create(user=user)
        elif account_type == 'organisation':
            OrganisationProfile.objects.create(user=user)
        
        return user 
            
    

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestorProfile
        fields = '__all__'
        read_only_fields = ['user']

        def create(self, validated_data):
            validated_data['user'] = self.context['request'].user
            return super().create(validated_data)


class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationProfile
        fields = '__all__'
        read_only_fields = ['user']

        def create(self, validated_data):
            validated_data['user'] = self.context['request'].user
            return super().create(validated_data)


class AddOrganisationToInvestorSerializer(serializers.ModelSerializer):
    organisation_id = serializers.IntegerField()

    def validate_organisation_id(self, value):
        if not OrganisationProfile.objects.filter(id=value).exists():
            raise serializers.ValidationError("Organisation does not exist.")
        return value
    
    def save(self, **kwargs):
        investor_profile = self.context['request'].user.investor_profile
        organisation = OrganisationProfile.objects.get(id=self.validated_data['organisation_id'])
        investor_profile.organisation.add(organisation)
        return organisation


class PersonalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalProfile
        fields = '__all__'
        read_only_fields = ['user']

        def create(self, validated_data):
            validated_data['user'] = self.context['request'].user
            return super().create(validated_data)